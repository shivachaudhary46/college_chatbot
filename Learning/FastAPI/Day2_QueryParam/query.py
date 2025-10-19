'''
When you declare other function params that are not part of the path parameters 
they are automatically intrepreted as Query parameters. 
'''

from fastapi import FastAPI

app = FastAPI() 
fake_db = [
    {
        "name": "shiva",
        "cllg": "MBMC College",
        "hobbies": "Learning new thing" 
    },
    {
        "name": "shiva1",
        "cllg": "MBMC College",
        "hobbies": "Learning new thing" 
    },
    {
        "name": "shiva2",
        "cllg": "MBMC College",
        "hobbies": "Learning new thing" 
    },
    {
        "name": "shiva3",
        "cllg": "MBMC College",
        "hobbies": "Learning new thing" 
    }
]

@app.get("/items")
async def get_all_items(i: int = 0, j : int = 10):
    items = fake_db[i: i+j]
    return {"items": items}

# @app.get("/items/{item_id}")
# async def optional_param(item_id: str, q: str | None = None, short: bool = False):
#     result = {"item_id": item_id}
#     if q: 
#         result.update({"q": q})
        
#     if not short:
#         result.update({"message": "This message is shit"})
#     return result 

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int =0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}

    return item
