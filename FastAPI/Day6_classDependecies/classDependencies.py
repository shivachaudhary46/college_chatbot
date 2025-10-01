from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI() 

async def callable(q: str, start: int | None = None, limit: int | None = None):
    return {
        "q": q,
        "start": start,
        "limit": limit
    }

@app.post("/items/")
async def dictDependency(commons: Annotated[str, Depends(callable)]):
    print("commons : ", type(commons))
    print("commons : ", commons)
    return commons