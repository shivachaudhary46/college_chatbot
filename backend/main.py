from typing import Annotated 
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# create a Hero table 
class store(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    full_name: str = Field(index=True)
    email: str = Field(default=None, index=True)
    hashed_password: str | None = Field(default = None)
    disabled: bool = False

# create an engine 
sqlite_file_name = "./database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# create a session 
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI() 

@app.on_event("startup")
def on_startup():
    create_db_and_tables() 

@app.post("/register/")
def create_one_db(DB: store, session: SessionDep) -> store:
    session.add(DB)
    session.commit()
    session.refresh(DB)
    return DB

# read all hero 
@app.get("/register/")
def read_all_db(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[store]:
    DB = session.exec(select(store).offset(offset).limit(limit)).all()
    return DB

# read one hero 
@app.get("/register/{user_id}")
def read_db(user_id: int, session: SessionDep) -> store:
    hero = session.get(store, user_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero 

# Delete Heroes
@app.delete("/register/{user_id}")
def delete_one_db(user_id: int, session: SessionDep):
    hero = session.get(store, user_id)
    if not hero: 
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}





