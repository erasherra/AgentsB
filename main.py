from typing import Union

from fastapi import WebSocket, Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
import json

from config import models
from project.utils.input_validator import validate_process_json
from project.utils.input_validator import validate_node
from project.process.multi_agent_system import MultiAgentSystem
from project.llms.model_manager import ModelManager
from project.llms.gpt import OpenAI
from project.llms.ollama import Ollama

import os



app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_manager = None
MAS = None
local_setup_json = None

def initialize_model_manager():
    global model_manager
    model_manager = ModelManager()
    
    for model in models:
        if model["name"] == "Ollama":
            model_manager.add_model("Ollama", Ollama(api_key="", model=model["model"]))
        elif model["name"] == "OpenAI":
            # Fix embedchain bug with better workaround
            os.environ["OPENAI_API_KEY"] = model["api_key"]
            model_manager.add_model("OpenAI", OpenAI(api_key=model["api_key"], model=model["model"]))
    
def initialize_setup():
    
    initialize_model_manager()
    
    with open("process.json", 'r') as f:
        local_setup_json = json.load(f)
    if not validate_process_json(local_setup_json):
        return {"message": "Invalid node data."}
    global MAS
    MAS = MultiAgentSystem(local_setup_json, model_manager=model_manager)
    return {"message": "Multi-agent system initialized successfully"}


@app.get("/")
def read_root():
    return {"Hello": "World123"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# In work
@app.post("/local_init")
async def init_multi_agent_system(request: Request) -> None:
    respnse = initialize_setup()
    return respnse

# In work
@app.post("/init")
async def init_multi_agent_system(request: Request) -> None:

    print("/init POST", request)
    initialize_model_manager()
    data = await request.json()
    print(data)
    if not validate_process_json(data):
        return {"message": "Invalid *.json file."}
    global MAS 
    MAS = MultiAgentSystem(data, model_manager=model_manager)
    return {"message": "Multi-agent system initialized successfully"}

# In work
@app.post("/process")
async def process_input(request: Request) -> None:
    data = await request.json()
    query = data["query"]
    #if MAS is None:
    #    initialize_setup()
    input_data, memory = MAS.process_input(query)
    return {"input_data": input_data, "memory": memory}


# In work
@app.post("/v2/process")
async def process_input_V2(request: Request) -> None:
    data = await request.json()
    query = data["query"]
    #if MAS is None:
    #    initialize_setup()
    input_data, memory = MAS.process_input(query)
    return {"input_data": input_data, "memory": memory}


@app.put("/modify/{node_id}")
def modify_agent(node_id: str, node_data: dict) -> None:
    if MAS is None:
        initialize_setup()
    if not validate_node(node_data):
        return {"message": "Invalid node data."}
    MAS.modify_agent(node_id, node_data)
    return {"message": "Agent modified successfully"}

# In work
@app.get("/models")
def get_models():
    return {"models": models}

# In work
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    exec_switch = True
    while True:
        if exec_switch:
            exec_switch = False
            input_data = await websocket.receive_text()
            print("ASD ", input_data)
            await MAS.process_input_stream(input_data, websocket)
            #await websocket.send_text(f"Message text was: {data}")
            exec_switch = True

if __name__ == "__main__":
    initialize_setup()
    print("Running...")
    # Add more code here if desired