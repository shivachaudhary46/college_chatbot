'''
To install fastapi 
$ pip install "fastapi[standard]"
'''

from pydantic import BaseModel
from fastapi import FastAPI
from enum import Enum

app = FastAPI() 

@app.post("/items/{item_id}")
async def get_items(item_id : int):
    return {"item_id": item_id}

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "The model name is alexnet"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "This model name is lesnet"}
    
    return {"model_name": model_name, "message": "this message will come when user does not choose alexnet and lesnet"}

@app.get("/files/{file_path}")
async def path_holder(file_path: str):
    return {"file_path": file_path}