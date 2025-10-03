from fastapi import FastAPI, Header
from typing import Annotated

app = FastAPI() 

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"user_agent": user_agent}