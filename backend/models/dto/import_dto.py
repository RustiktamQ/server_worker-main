from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict

from models.server import DatabaseServer


class ImportDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    upload_file: UploadFile
    table_name: str
    schema_name: str
    server_id: int
