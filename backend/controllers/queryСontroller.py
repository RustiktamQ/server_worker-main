import json
from typing import Annotated, List, Union
from fastapi import File, Form, HTTPException, Request, Response, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from services.import_service import ImportService
from dependencies.services_dependency import get_db_servers, get_import_service
from models.server import DatabaseServer
from fastapi import APIRouter, Depends
from dependencies.services_dependency import (
    get_export_service,
    get_query_service,
    get_translite_service,
)
from models.dto.import_dto import ImportDTO
from models.dto.export_dto import ExportDTO
from services.export_service import ExportService
from services.query_service import QueryService
from services.translite_service import TransliteService
from models.dto.send_query_dto import SendQueryDTO
from services.logger_service import logger

router = APIRouter()


@router.get("/servers")
async def get_servers(db_servers: List[DatabaseServer] = Depends(get_db_servers)):
    logger.info("Получаем список серверов")
    return db_servers


@router.post("/execute")
async def execute_query(
    dto: SendQueryDTO, queryService: QueryService = Depends(get_query_service)
):
    try:
        logger.info("Выполняем SQL запрос...")
        results = await queryService.run_query(dto)
        logger.info("SQL запрос выполнен!")
        return results
    except Exception as e:
        logger.error(f"Не удалось выполнить SQL: {e}")
        return JSONResponse(
            status_code=500, content={"detail": f"Ошибка при выполнении запроса: {e}"}
        )


@router.post("/import")
async def import_data(
    dto: Annotated[ImportDTO, Form()],
    importService: ImportService = Depends(get_import_service),
):
    try:
        logger.error("Выполняем импорт...")
        results = await importService.import_to_server(dto)
        logger.info("Импорт выполнен!")
        return results
    except Exception as e:
        logger.error(f"Не удалось совершить импорт: {e}")
        return JSONResponse(
            status_code=500, content={"detail": f"Ошибка при импорте данных: {e}"}
        )
    
@router.post("/import/preview")
async def preview_file(
    file: UploadFile = File(...),
    importService: ImportService = Depends(get_import_service),
):
    try:
        logger.info(f"Предпросмотр файла: {file.filename}")
        df = await importService._read_file(file)
        if df is None:
            raise HTTPException(status_code=400, detail="Не удалось прочитать файл")
        preview = {
            "headers": df.columns.tolist(),
            "rows": df.head(50).fillna("").astype(str).values.tolist(),
        }
        logger.info(f"Файл {file.filename} успешно обработан для предпросмотра")
        return JSONResponse(content=preview)

    except Exception as e:
        logger.error(f"Ошибка предпросмотра файла {file.filename}: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Ошибка при обработке файла: {e}"},
        )

@router.post("/export")
async def export_data(
    request: Request, exportService: ExportService = Depends(get_export_service)
):
    try:
        logger.info("Выполняем экспорт...")
        payload = await request.json()
        if isinstance(payload, str):
            payload = json.loads(payload)

        dto = ExportDTO(**payload)
        result = exportService.export(dto)

        headers = {
            "Content-Disposition": f'attachment; filename="{result.filename}"',
            "Content-Type": result.mime,
            "Content-Length": str(len(result.content)),
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }

        logger.info(f"Экспорт выполнен!")
        return Response(content=result.content, media_type=result.mime, headers=headers)

    except Exception as e:
        logger.error(f"Не удалось совершить экспорт: {e}")
        return JSONResponse(
            status_code=500, content={"detail": f"Ошибка при экспорте данных: {e}"}
        )


# - - - - - - - - - TEST - - - - - - - - - - - - -


@router.get("/test", response_class=HTMLResponse)
async def test():
    return """
    <html>
        <head>
            <title>123</title>
        </head>
        <body>
            <a href="/test/translite/Проверяем транслит!:*">Проверить translite</a><br>
            <a href="/test/execute">Проверить execute</a><br>
            <a href="/test/export">Проверить export</a><br>
            <a href="/test/import">Проверить import</a><br>
        </body>
    </html>
    """


@router.get("/test/translite/{text}")
async def translite(
    text: Union[str, None] = None,
    translitService: TransliteService = Depends(get_translite_service),
):
    results = translitService.translite(text)
    return results


@router.get("/test/execute", response_class=FileResponse)
async def test_query_page():
    return "../frontend/src/test/test.html"


@router.get("/test/export", response_class=FileResponse)
async def test_export_page():
    return "../frontend/src/test/test.html"


@router.get("/test/import", response_class=FileResponse)
async def test_import_page():
    return "../frontend/src/test/import.html"
