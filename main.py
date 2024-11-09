from typing import Union

from fastapi import WebSocket, Request, FastAPI
import json
from project.utils.input_validator import validate_process_json
from project.utils.input_validator import validate_node
from project.process.multi_agent_system import MultiAgentSystem

app = FastAPI()

ms = None
local_setup_json = None

@app.get("/")
def read_root():
    return {"Hello": "World123"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/local_init")
async def init_multi_agent_system(request: Request) -> None:
    respnse = initialize_setup()
    return respnse

@app.post("/init")
async def init_multi_agent_system(request: Request) -> None:

    data = request.json()
    if not validate_process_json(data):
        return {"message": "Invalid *.json file."}
    ms = MultiAgentSystem(data, model_manager=None)
    return {"message": "Multi-agent system initialized successfully"}


@app.post("/process")
def process_input(input_data: dict) -> tuple:
    if ms is None:
        initialize_setup()
    input_data, memory = ms.process_input(input_data)
    return {"input_data": input_data, "memory": memory}


@app.put("/modify/{node_id}")
def modify_agent(node_id: str, node_data: dict) -> None:
    if ms is None:
        initialize_setup()
    if not validate_node(node_data):
        return {"message": "Invalid node data."}
    ms.modify_agent(node_id, node_data)
    return {"message": "Agent modified successfully"}


@app.get("/models")
def get_models():
    return {"Hello": "TODO"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        input_data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")



def initialize_setup():
    
    with open("process.json", 'r') as f:
        local_setup_json = json.load(f)
    if not validate_process_json(local_setup_json):
        return {"message": "Invalid node data."}
    ms = MultiAgentSystem(local_setup_json, model_manager=None)
    return {"message": "Multi-agent system initialized successfully"}

if __name__ == "__main__":
    initialize_setup()
    print("Running...")
    # Add more code here if desired