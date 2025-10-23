from pydantic import BaseModel, ConfigDict
from models.server import DatabaseServer


class SendQueryDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    query: str
    selected_server: DatabaseServer
