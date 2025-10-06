from .database import SessionDep, create_all_db_tables
from .models import User
from sqlmodel import select

from typing import Annotated
from fastapi import FastAPI, Query, HTTPException

app = FastAPI() 

@app.on_event("startup")
def on_startup():
    create_all_db_tables()

'''
create an account 
'''
@app.post("/create_an_account/")
def create_an_account(user: User, session: SessionDep) -> User:
    user.set_password(user.hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

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





