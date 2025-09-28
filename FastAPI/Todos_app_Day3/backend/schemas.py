from pydantic import BaseModel, Field
from datetime import datetime as dt
from typing import Optional

class moreInfo(BaseModel):
    priority: str 
    created_at: dt = Field(default_factory=dt.now())

class Item(BaseModel):
    title: str 
    description: str | None = None
    completed: bool = False
    info: moreInfo 

