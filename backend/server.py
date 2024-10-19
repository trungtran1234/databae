from fastapi import FastAPI, Request
from uagents import Model
from uagents.query import query
from uagents.envelope import Envelope
import json

# Agent address
AGENT_ADDRESS = "agent1qtafwkkm26h5gdkkz39pd5nnt604q96xh4hperynl085cwzquh0uyunffjz"

app = FastAPI()

# Define request model
class TestRequest(Model):
    message: str

# Function to send query to agent and get response
async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=5)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return data["text"]
    return response

@app.get("/")
def read_root():
    return "Hello from the Agent controller"

@app.post("/endpoint")
async def make_agent_call(req: Request):
    try:
        model = TestRequest.parse_obj(await req.json())
        res = await agent_query(model)
        return {"status": "successful", "agent_response": res}
    except Exception as e:
        return {"status": "unsuccessful", "error": str(e)}
