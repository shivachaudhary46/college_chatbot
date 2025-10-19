# from fastapi import FastAPI, Request
# from typing import Annotated
# from . import schemas
# import time
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI() 

# next_id = 1
# fake_db = {

# }

# origins = [
#     "http://127.0.0.1:5500/Todos_app_Day3-4/frontend/",
#     "http://127.0.0.1:8000/",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.post("/items/{item_id}")
# async def create_item(item_id: int, item: schemas.Item):
#     item = item.dict()
#     fake_db.update({item_id: item})
#     return {
#         "message": f"successfully uploaded {item_id} to database",
#         "status": "success",
#         "database": fake_db[item_id]
#     }
