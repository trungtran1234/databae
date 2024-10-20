from uagents import Model
from typing import Any, Optional

class Request(Model):
    query: str
    user: str = None

class Response(Model):
    text: str
    query: Optional[str] = None
    sqlschema: Optional[dict] = None
    user: Optional[str] = None
    table: Optional[Any] = None

    class Config:
        # Include fields with None values during serialization
        exclude_none = False
