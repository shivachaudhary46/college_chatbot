from fastapi import FastAPI, Depends, Cookie
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

fake_item_db = [
    {"name": "shiva"},
    {"name": "jevis"},
    {"name": "samprad"},
    {"name": "chandan"}
]

class commonQueryParameters:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q 
        self.skip = skip 
        self.limit = limit 

@app.get("/items/")
async def read_items(common: Annotated[commonQueryParameters, Depends(commonQueryParameters)]):
    response = {}
    if common.q:
        response.update({"q": common.q})
    items = fake_item_db[common.skip : common.skip + common.limit]
    response.update({"item": items})
    return response

def query(q: str | None = None):
    return q 

def query_or_cookie(q: Annotated[str | None, Depends(query)], 
                    cookie: Annotated[str | None, Cookie()] = None):
    if not q:
        return cookie
    return q 

@app.get("/read_query/")
async def read_quer(query_or_default: Annotated[query_or_cookie, Depends()]):
    return query_or_default
