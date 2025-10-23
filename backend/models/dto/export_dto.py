from typing import Any, Literal
from pydantic import BaseModel, ConfigDict


class ExportDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data: Any
    format: Literal["excel", "json", "csv"]
