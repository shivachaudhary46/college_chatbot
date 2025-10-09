from pydantic import BaseModel, EmailStr
from fastapi import FastAPI

app = FastAPI() 

# class User_In(BaseModel):
#     username: str
#     email: EmailStr | None = None 
#     password: str
#     full_name: str | None = None

# class User_Out(BaseModel):
#     username: str
#     email: EmailStr | None = None
#     full_name: str | None = None

# class UserInDB(BaseModel):
#     username: str
#     email: EmailStr | None = None
#     full_name: str | None = None
#     hashed_password: str

# Instead of doing code duplication we can inherit the base model and it will
# work same and it does not need code duplication. 

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def fake_hash_password(plain_password: str):
    return "hashed" + plain_password

def save_fake_user(user: UserIn):
    hashed_password = fake_hash_password(user.password)
    user = UserInDB(
        **user.dict(), hashed_password=hashed_password
    )
    print("saved user in database")
    return user

@app.post("/register/", response_model=UserOut)
async def create_username(user: UserIn):
    return save_fake_user(user)

