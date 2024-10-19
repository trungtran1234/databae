from uagents import Model

class Request(Model):
    query: str
    user: str = None

class Response(Model):
    text: str
    query: str = None
    sqlschema: dict = None
    user: str = None
