from typing import NamedTuple


class ExportResult(NamedTuple):
    content: bytes
    mime: str
    filename: str
