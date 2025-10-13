# =============  Models for login backend ===========================================================
# ============= *************************  ============================================================
'''
This is the production level backend
'''

# ============== Login backend imports =============
from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated, Optional
from pydantic import BaseModel

from pwdlib import PasswordHash

from datetime import datetime

hasher = PasswordHash.recommended()

# =============== Usermodel table ==================
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(index=True, unique=True)
    full_name: str 
    email: str 
    hashed_password: str 
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
# ================ User Info =======================
class Info(SQLModel):
    username: str | None = Field(index=True, unique=True)
    full_name: str 
    email: str 
    hashed_password: str 
    disabled: bool = Field(default=False)

    def set_password(self, plain_password: str):
        self.hashed_password = hasher.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return hasher.verify(plain_password, hashed_password)

# ======= JWT token info ================== 
class Token(BaseModel):
    access_token: str
    token_type: str

# ====== Token Data ======================
class Token_Data(BaseModel):
    username: str

# ====== for storing Hashed Password ===================
class UserInDB(User):
    hashed_password: str

# ====== username from database ===================
def get_user(db, username: str):
    if username in db:
        user = db[username]
        return UserInDB(**user)
    
# =========== verifying hashed password ===================
def verify_password(password, hashed_password):
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hashed_password) # if match return True, If not then False
    
# =========== Authenticate username =====================
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
