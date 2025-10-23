from typing import Any, List, Union
from pydantic import BaseModel


class QueryResult(BaseModel):
    server: str
    status: str
    message: Union[str, None] = None
    data: List[Any] = []
    time: Union[str, None] = None
