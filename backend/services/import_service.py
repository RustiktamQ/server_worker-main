from models.dto.send_query_dto import SendQueryDTO
from services.query_service import QueryService
from models.server import DatabaseServer
from models.dto.import_dto import ImportDTO
from models.dto.query_result import QueryResult
from services.translite_service import TransliteService
from typing import List, Union
import time
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import io
import os
from fastapi import UploadFile
from typing import Literal
from services.logger_service import logger


class ImportService:
    def __init__(
        self,
        db_servers: List[DatabaseServer],
        translite_service: TransliteService,
        query_service: QueryService,
    ):
        self.translite_service = translite_service
        self.query_service = query_service
        self.SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv", ".json"}
        self.db_servers = db_servers

        self._servers_by_id = {s.id: s for s in db_servers}

    async def import_to_server(self, dto: ImportDTO) -> QueryResult:
        df = await self._read_file(dto.upload_file)

        if df is None:
            return self._failed("unknown", "Не удалось прочитать файл")

        df = self._transliterate_columns(df)

        if dto.server_id in self._servers_by_id:
            server = self._servers_by_id[dto.server_id]

            create_sql = self._generate_create_table_sql(
                df, dto.table_name, dto.schema_name, server.type
            )

            result = await self._execute_on_single_server(
                create_sql, df, dto.table_name, dto.schema_name, server
            )

            return result
        else:
            return self._failed("unknown", "Сервер не найден")

    def _failed(self, server_name: str, message: str) -> QueryResult:
        logger.error(f"Сервер '{server_name}' вернул ошибку: {message}")
        return QueryResult(server=server_name, status="error", message=message)

    async def _read_file(self, upload_file: UploadFile) -> Union[pd.DataFrame, None]:
        try:
            content = await upload_file.read()
            filename = upload_file.filename
            if filename is None:
                raise ValueError("Неподдерживаемое имя файла")

            file_type = self._detect_file_type(filename)

            if file_type == "excel":
                return pd.read_excel(io.BytesIO(content))
            elif file_type == "csv":
                return pd.read_csv(io.BytesIO(content), encoding="utf-8")
            elif file_type == "json":
                return pd.read_json(io.BytesIO(content), encoding="utf-8")
        except ValueError as ve:
            logger.error(str(ve))

    def _detect_file_type(self, filename: str) -> str:
        _, ext = os.path.splitext(filename.lower())
        if ext in [".xlsx", ".xls"]:
            return "excel"
        elif ext == ".csv":
            return "csv"
        elif ext == ".json":
            return "json"
        else:
            raise ValueError(f"Неподдерживаемое расширение файла: {ext}")

    def _transliterate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        translated_columns = []
        for col in df.columns:
            latin_col = self.translite_service.translite(str(col))
            translated_columns.append(latin_col)
        df.columns = translated_columns
        return df

    def _generate_create_table_sql(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema_name: str,
        dialect: Literal["mysql", "postgresql", "oracle"],
    ) -> List[str]:
        columns = []
        for col in df.columns:
            series = df[col]
            sql_type = self._define_sql_type(series, dialect)
            columns.append(f"{col} {sql_type}")

        columns_def = ", ".join(columns)
        sql_commands = []

        if dialect == "mysql":
            sql_commands = [
                f"CREATE DATABASE IF NOT EXISTS {schema_name}",
                f"USE {schema_name}",
                f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})",
            ]

        elif dialect == "postgresql":
            sql_commands = [
                f"CREATE SCHEMA IF NOT EXISTS {schema_name}",
                f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({columns_def})",
            ]

        elif dialect == "oracle":
            sql_commands = [
                f"""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE USER {schema_name} IDENTIFIED BY password';
                EXCEPTION
                    WHEN OTHERS THEN NULL;
                END;
                """,
                f"CREATE TABLE {schema_name}.{table_name} ({columns_def})",
            ]

        else:
            raise ValueError(f"Недопустимый тип: {dialect}")

        return sql_commands

    def _define_sql_type(
        self, series: pd.Series, dialect: Literal["mysql", "postgresql", "oracle"]
    ) -> str:
        non_null = series.dropna()
        if non_null.empty:
            return self._get_varchar_type(dialect, 255)
        if pd.api.types.is_integer_dtype(non_null):
            return self._get_integer_type(non_null, dialect)
        elif pd.api.types.is_float_dtype(non_null):
            return self._get_float_type(dialect)
        elif pd.api.types.is_bool_dtype(non_null):
            return self._get_boolean_type(dialect)
        elif pd.api.types.is_datetime64_any_dtype(non_null):
            return self._get_datetime_type(dialect)
        else:
            max_len = non_null.astype(str).map(len).max()
            return self._get_varchar_type(dialect, max_len)

    def _get_varchar_type(self, dialect: str, max_len: int) -> str:
        length = min(max_len * 2, 4000)
        if dialect == "oracle":
            if length <= 4000:
                return f"VARCHAR2({length})"
            else:
                return "CLOB"
        elif dialect in ["mysql", "mariadb"]:
            if length <= 65535:
                return f"VARCHAR({length})"
            else:
                return "TEXT"
        elif dialect == "postgresql":
            if length <= 10485760:
                return f"VARCHAR({length})"
            else:
                return "TEXT"
        else:
            return "TEXT"

    def _get_integer_type(self, series: pd.Series, dialect: str) -> str:
        if dialect == "oracle":
            if series.between(-32768, 32767).all():
                return "NUMBER(5)"
            elif series.between(-8388608, 8388608).all():
                return "NUMBER(7)"
            elif series.between(-2147483648, 2147483647).all():
                return "PLS_INTEGER"
            else:
                return "NUMBER(19)"
        elif dialect == "postgresql":
            if series.between(-32768, 32767).all():
                return "smallint"
            elif series.between(-2147483648, 2147483647).all():
                return "integer"
            else:
                return "bigint"
        else:
            if series.between(-32768, 32767).all():
                return "SMALLINT"
            elif series.between(-8388608, 8388608).all():
                return "MEDIUMINT"
            elif series.between(-2147483648, 2147483647).all():
                return "INT"
            else:
                return "BIGINT"

    def _get_float_type(self, dialect: str) -> str:
        if dialect == "oracle":
            return "BINARY_DOUBLE"
        elif dialect == "postgresql":
            return "DOUBLE PRECISION"
        else:
            return "DOUBLE"

    def _get_boolean_type(self, dialect: str) -> str:
        if dialect == "oracle":
            return "NUMBER(1)"
        else:
            return "BOOLEAN"

    def _get_datetime_type(self, dialect: str) -> str:
        if dialect == "mysql":
            return "DATETIME"
        else:
            return "TIMESTAMP"

    def _execute_on_servers(
        self,
        create_sql: str,
        df: pd.DataFrame,
        table_name: str,
        schema_name: str,
        servers: List[DatabaseServer],
    ) -> List[QueryResult]:
        results = []
        for _, server in enumerate(servers, 1):
            server_name = server.name
            try:
                dialect = server.type
                engine_url = f"{dialect}://{server.username}:{server.password}@{server.host}:{server.port}/{server.database}"
                engine = create_engine(engine_url)

                with engine.connect() as conn:
                    conn.execute(text(create_sql.lower()))
                    conn.commit()

                start_time = time.time()

                df.to_sql(
                    name=table_name,
                    con=engine,
                    schema=schema_name,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=1000,
                )

                load_time = time.time() - start_time
                results.append(
                    QueryResult(
                        server=server_name,
                        status="success",
                        message=f"Импорт выполнился за {load_time}",
                        time=f"{round(load_time, 3)}",
                    )
                )

            except SQLAlchemyError as e:
                results.append(self._failed(server_name, f"SQLAlchemyError: {e}"))

            except Exception as e:
                results.append(
                    self._failed(server_name, f"Не удалось сделать импорт: {e}")
                )

        return results

    async def _execute_on_single_server(
        self,
        create_sql: List[str],
        df: pd.DataFrame,
        table_name: str,
        schema_name: str,
        server: DatabaseServer,
    ) -> QueryResult:
        server_name = server.name
        engine = None
        try:
            for sql_command in create_sql:
                dto = SendQueryDTO(query=sql_command, selected_server=server)
                result = await self.query_service.run_query(dto)
                if result.status != "success":
                    logger.warning(
                        f"Предупреждение: команда '{sql_command}' завершилась со статусом {result.status}"
                    )

            dialect = server.type
            if dialect in ["mysql", "mariadb"]:
                engine_url = f"{dialect}+pymysql://{server.username}:{server.password}@{server.host}:{server.port}/{server.database}"
            elif dialect == "postgresql":
                engine_url = f"{dialect}+psycopg2://{server.username}:{server.password}@{server.host}:{server.port}/{server.database}"
            elif dialect == "oracle":
                engine_url = f"{dialect}+oracledb://{server.username}:{server.password}@{server.host}:{server.port}/?service_name={server.database}"
            else:
                engine_url = f"{dialect}://{server.username}:{server.password}@{server.host}:{server.port}/{server.database}"

            engine = create_engine(engine_url)

            start_time = time.time()

            df.to_sql(
                name=table_name.lower(),
                con=engine,
                schema=schema_name.lower(),
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )

            load_time = time.time() - start_time
            return QueryResult(
                server=server_name,
                status="success",
                message=f"Импорт выполнился!",
                time=f"{round(load_time, 3)}"
            )

        except SQLAlchemyError as e:
            return self._failed(server_name, f"SQLAlchemyError: {e}")
        except Exception as e:
            return self._failed(server_name, f"Не удалось сделать импорт: {e}")
        finally:
            if engine:
                engine.dispose()
