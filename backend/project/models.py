from sqlmodel import SQLModel, Field
from typing import Annotated 
from pwdlib import PasswordHash

hasher = PasswordHash.recommended()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(index=True, unique=True)
    full_name: str 
    email: str 
    hashed_password: str 
    disabled: bool = Field(default=False)

    def set_password(self, plain_password: str):
        self.hashed_password = hasher.hash(plain_password)

