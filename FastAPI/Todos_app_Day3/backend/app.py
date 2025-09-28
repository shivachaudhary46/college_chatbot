from fastapi import FastAPI 
from typing import Annotated
from . import schemas

app = FastAPI() 

next_id = 1
fake_db = {

}


@app.post("/items/{item_id}")
async def create_item(item_id: int, item: schemas.Item):
    item = item.dict()
    fake_db.update({item_id: item})
    return {
        "message": f"successfully uploaded {item_id} to database",
        "status": "success",
        "database": fake_db[item_id]
    }