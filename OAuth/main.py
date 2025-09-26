from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

"""  
# what is OpenAPI for 
OpenAPI is just like a blueprint or map of API. 
which describes the what API can do (simply absract them)
Example: if your API has /items/ that returns a list of items 
then it writes down in (JSON) format. 

#What is OpenAPI + JSON Schema
OpenAPI is about the API structure (endpoints, methods, responses)
while in inside it uses JSON schema to describe the shape of the data. 

Here's how you can check OpenAPI:
http://127.0.0.1:8000/openapi.json

you'll see the raw json blueprint of API. but, It looks scary.
{
    "openapi":"3.1.0",
    "info":{"title":"FastAPI","version":"0.1.0"},
    "paths":{"/":
        {"get":
            {"summary":"Root","operationId":"root__get","responses":
                {"200":
                    {"description":"Successful Response","content":
                        {"application/json":{"schema":{}}
                    }
                }
            }
        }
    }
}

"""

""" 
# The simplest FastAPI call 
 @app.get("/") tells FastAPI that the function right below is in charge of requests
 the path / & using a get operation. 
 you can also use other operation like 

 @app.post() to create data
 @app.put() to update data
 @app.delete() to delete data

"""

"""
every one is using async right do you know what is it ? 
Async means asynchronous which is you can run other program while your request waiting. 

when your API does something slow like (waiting for a database, calling another api)
normally, Python would just sit and wait. 

when using async, FastAPI can do other work not just block the server and handle other requests in the mean time. 
"""

"""
In async function
you can return a dict, list, singular values as str, int etc. 
"""

'''
If you want a specific parameter with free from error prone
then you can use path parameter to predefined value. you can use a standard python Enum 
'''

# from enum import Enum

# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning model"}
    
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

''' 
When you don't implement the function parameter that are not of the path
parameters, then they are automatically intrepreted as 'query' parameter 

If you need any help then go to documentation https://fastapi.tiangolo.com/tutorial/query-params/
We can add the default parameter in the query parameter. 
'''
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

'''
There are other ways also to set optional parameter, for example: giving default value as None
even if you don't fill the optional parameter the value set is None, so it will not give any type of error.
'''
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

''' 
you can also declare the bool types, and they will be converted.
# Go to Query Parameter Type Conversion 
'''
# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item

from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import BaseModel
import random
from pydantic import AfterValidator

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/items/")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}


