from uagents import Model

class Request(Model):
    query: str

class Response(Model):
    text: str
    query: str = None
    sqlschema: dict = None

class UserRequest(Model):
    message: str
