from .database import SessionDep, create_all_db_tables
from .models import User, Token, Info
from sqlmodel import select
from datetime import timedelta

from typing import Annotated
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .utilities import authenticate_user, create_access_token, get_current_user
from dotenv import load_dotenv
import os 

load_dotenv()

ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE"))

app = FastAPI() 

@app.on_event("startup")
def on_startup():
    create_all_db_tables()

'''
create an account 
'''
@app.post("/create_an_account/")
def create_an_account(info: Info, session: SessionDep):
    info.set_password(info.hashed_password)
    user = User(**info.model_dump())
    session.add(user)
    session.commit()

    info.hashed_password = ""
    return info

'''
read all account
'''
@app.get("/create_an_account/")
def read_all_account(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    statement = select(User).offset(offset).limit(limit)
    results = session.exec(statement)
    accounts = results.all()
    return accounts

'''
read one account
'''
@app.get("/create_an_account/{username}")
def read_one_account(username: str, session: SessionDep) -> User:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    account = results.one()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not Found")
    return account 

'''
Delete one account
'''
@app.delete("/create_an_account/{username}")
def delete_one_account(username: str, session: SessionDep):
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    account = results.one()

    if not account: 
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(account)
    session.commit()
    return {"ok": True}

'''
Login with token
'''
@app.post("/token")
async def login_an_account(data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = authenticate_user(data.username, data.password, session)
    if not user: 
        raise HTTPException(status_code=400, detail="invalid Username or password")
    
    access_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    token = create_access_token(
        data = {"sub": user.username}, expire_time = access_time
    )

    if token is None :
        raise HTTPException(status_code=400, detail="invalid username or password")

    return Token(access_token=token, token_type="bearer")

'''
show current user
'''
@app.get("/token")
async def get_current_username(current_user: Annotated[User, Depends(get_current_user)]):
    return {"user": current_user.username}

