import json
import os
from fastapi import Depends
from typing import List
from services.export_service import ExportService
from services.import_service import ImportService
from models.server import DatabaseServer
from services.translite_service import TransliteService
from services.query_service import QueryService


def get_db_servers() -> List[DatabaseServer]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "..", "servers.json")

    try:
        with open(json_path, "r") as file:
            servers_data = json.load(file)

        db_servers = []
        for server in servers_data:
            db_servers.append(
                DatabaseServer(
                    id=server["id"],
                    name=server["name"],
                    host=server["host"],
                    port=server["port"],
                    username=server["username"],
                    password=server["password"],
                    database=server["database"],
                    type=server["type"],
                )
            )

        return db_servers

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл конфигурации не найден: {json_path}")

    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка формата JSON в файле {json_path}: {e}")

    except KeyError as e:
        raise ValueError(f"Отсутствует обязательное поле в конфигурации: {e}")

    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла: {json_path}")

    except Exception as e:
        raise RuntimeError(f"Неперехваченная ошибка: {e}")


def get_query_service(
    db_servers: List[DatabaseServer] = Depends(get_db_servers),
) -> QueryService:
    return QueryService(db_servers)


def get_translite_service() -> TransliteService:
    return TransliteService()


def get_import_service(
    db_servers: List[DatabaseServer] = Depends(get_db_servers),
    queryService: QueryService = Depends(get_query_service),
) -> ImportService:
    return ImportService(db_servers, get_translite_service(), queryService)


def get_export_service() -> ExportService:
    return ExportService()
