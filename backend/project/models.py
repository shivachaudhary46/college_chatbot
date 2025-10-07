from sqlmodel import SQLModel, Field
from typing import Annotated 
from pydantic import BaseModel
from pwdlib import PasswordHash

hasher = PasswordHash.recommended()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(index=True, unique=True)
    full_name: str 
    email: str 
    hashed_password: str 
    disabled: bool = Field(default=False)
    
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

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_Data(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user = db[username]
        return UserInDB(**user)
    
def verify_password(password, hashed_password):
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hashed_password) # if match return True, If not then False
    
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
