from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List

# ===== User Schemas =====
class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    batch: str
    program: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    batch: str
    program: str
    created_at: datetime

    class Config:
        from_attributes = True

