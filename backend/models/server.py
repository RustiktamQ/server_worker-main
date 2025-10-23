from pydantic import BaseModel
from typing import Literal


class DatabaseServer(BaseModel):
    id: int
    name: str
    host: str
    port: int
    username: str
    password: str
    database: str
    type: Literal["mysql", "postgresql", "oracle"]
