import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from uagents import Model
from uagents.query import query
from uagents.envelope import Envelope
import json
from db_tools import check_and_add_db_credentials
import agent_class
from fastapi.middleware.cors import CORSMiddleware

# Agent address
AGENT_ADDRESS = "agent1qtafwkkm26h5gdkkz39pd5nnt604q96xh4hperynl085cwzquh0uyunffjz"

app = FastAPI()

origins = [
    "http://localhost:3000",  # Your React app's origin
]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)



class DbBodyModel(BaseModel):
    host_name: str
    username: str
    password: str
    port: int
    db_name: str


async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=30)
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
        model = agent_class.Request.parse_obj(await req.json())
        res = await agent_query(model)

        if os.path.exists('response.txt'):
            with open('response.txt', "r") as file:
                file_content = file.read().replace("\n", "")
        else:
            file_content = "File not found"
        return {"status": "successful", "agent_response": file_content}
    except Exception as e:
        print(e)
        return {"status": "unsuccessful", "error": str(e)}

# endpoint that takes in database connection details,
# checks if there is the db connection is valid,
# saves it to db_credentials.json
# for now, the db has to have ssl off
# returns 404 if the database is not able to be connected to
@app.post("/input_connection_details")
async def input_connection_details(db: DbBodyModel):
    if check_and_add_db_credentials(db.host_name, db.username, db.password, db.port, db.db_name):
        return "success"
    else: 
        raise HTTPException(status_code=404, detail="Could not connect to database")
    
