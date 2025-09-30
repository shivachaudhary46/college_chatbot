from fastapi import FastAPI, Depends, HTTPException 
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
db = {}
iteration_counter = {"count": 0}

def track_iteration():
    iteration_counter["count"] += 1
    print(f"Iteration: {iteration_counter['count']}")
    return iteration_counter["count"]

class Item(BaseModel):
    title: str 
    description: str | None = None
    completed: bool = False 

@app.post("/items/{item_id}")
async def insert_item(
    item_id: int,
    item: Item,
    iteration: int = Depends(track_iteration)
):
    result = item.dict() 
    result["iteration"] = iteration  
    db.update({item_id: result})  
    return result

@app.get("/items")
async def read_all_item():
    return db

@app.get("/items/{item_id}")
async def read_one_item(item_id: int):
    result = db[item_id]
    return result

@app.put("/items/{item_id}")
async def update_one_data(item_id: int, item: Item):
    db[item_id] = item
    return db[item_id]

@app.delete("/items/{item_id}")
async def deleted(item_id: int):
    db.pop(item_id)
    return{"status": "deleted ok True"}
