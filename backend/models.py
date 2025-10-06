from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str | None = Field(index=True, unique=True)
    full_name: str 
    email: str 
    hashed_password: str 
    disabled: bool = Field(default=False)