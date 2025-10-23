from typing import List
import asyncio
import aiomysql
import asyncpg
import oracledb
import time
from models.dto.send_query_dto import SendQueryDTO
from models.dto.query_result import QueryResult
from models.server import DatabaseServer
from services.logger_service import logger


class QueryService:
    def __init__(
        self,
        db_servers: List[DatabaseServer],
        max_concurrent: int = 10,
        timeout_sec: int = 30,
    ):
        self.db_servers = db_servers
        self.max_concurrent = max_concurrent
        self.timeout_sec = timeout_sec

    # Необходимо использовать оракл клиент для поддержки асинхронных вызовов (Нереальная параша)
    # oracledb.init_oracle_client()

    async def run_query(self, dto: SendQueryDTO) -> QueryResult:
        if dto.selected_server.id not in [server.id for server in self.db_servers]:
            return self._failed(
                dto.selected_server.name,
                "Сервер не найден в конфиге",
            )

        sem = asyncio.Semaphore(self.max_concurrent)

        result = await self._run_one_with_guard(sem, dto.selected_server, dto.query)
        return result

    async def _run_one_with_guard(
        self, sem: asyncio.Semaphore, server: DatabaseServer, query: str
    ) -> QueryResult:
        async with sem:
            try:
                start_time = time.time()

                data = await asyncio.wait_for(
                    self._execute(server, query), timeout=self.timeout_sec
                )

                load_time = time.time() - start_time
                return QueryResult(
                    server=server.name,
                    status="success",
                    message="Запрос успешно выполнен",
                    data=data,
                    time=f"{round(load_time, 3)}",
                )

            except asyncio.TimeoutError:
                msg = f"Таймаут {self.timeout_sec}s"
                return self._failed(server.name, msg)

            except Exception as e:
                return self._failed(server.name, str(e))

    def _failed(self, server_name: str, message: str) -> QueryResult:
        logger.error(f"Сервер '{server_name}' вернул ошибку: {message}")
        return QueryResult(server=server_name, status="error", message=message)

    async def _execute(self, server: DatabaseServer, query: str) -> list[dict]:
        if server.type == "mysql":
            return await self._mysql_exec(server, query)
        elif server.type == "postgresql":
            return await self._pg_exec(server, query)
        elif server.type == "oracle":
            return await self._oracle_exec(server, query)
        else:
            raise ValueError(f"Неподдерживаемая СУБД: {server.type}")

    async def _mysql_exec(self, server: DatabaseServer, query: str) -> list[dict]:
        logger.info(f"Отправили на '{server.name}' mysql запрос")
        conn = await aiomysql.connect(
            host=server.host,
            port=server.port,
            user=server.username,
            password=server.password,
            db=server.database,
            autocommit=True,
        )
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()
                return rows or []
        finally:
            conn.close()

    async def _pg_exec(self, server: DatabaseServer, query: str) -> list[dict]:
        logger.info(f"Отправили на '{server.name}' postgre запрос")
        conn_str = f"postgresql://{server.username}:{server.password}@{server.host}:{server.port}/{server.database}"
        conn = await asyncpg.connect(conn_str)
        try:
            rows = await conn.fetch(query)
            return [dict(r) for r in rows] if rows else []
        finally:
            await conn.close()

    async def _oracle_exec(self, server: DatabaseServer, query: str) -> list[dict]:
        logger.info(f"Отправили на '{server.name}' oracle запрос")
        dsn = f"{server.host}:{server.port}/{server.database}"

        async with oracledb.connect_async(
            user=server.username, password=server.password, dsn=dsn
        ) as connection:
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(query)
                    rows = await cursor.fetchall()

                    if rows:
                        columns = [col[0] for col in cursor.description]
                        return [dict(zip(columns, row)) for row in rows]
                    return []
            finally:
                await connection.close()
