from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends, HTTPException, Query

'''Create the App wjth a Single Model'''
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str 

'''Create an Engine'''
sqlite_file_name = "./database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

'''It allows FastAPI to use the same SQLite database on the different threads'''
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

'''Create the Tables'''
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

'''Create a Session Dependency'''
'''A session is what stores the objects in memory
and keeps tracks of any changes needed in the data. 
then it uses the enginge to communicate with the database.'''
def get_session():
    with Session(engine) as session:
        yield session

'''Annotated Dependency'''
SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

'''Create Database Tables on Startup'''
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

'''Create a Hero'''
'''If you declare a parameter of type Hero, it will read for the JSON body.'''
@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero : 
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

'''Read Heroes'''
@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    Limit: Annotated[int, Query(le=100)] = 100
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(Limit)).all()
    return heroes

'''Read One Heroes'''
@app.get("/heroes/{hero_id}")
def  read_hero(hero_id: int, session: SessionDep) -> Hero : 
    hero = Session.get(Hero, hero_id)
    if not hero: 
        raise HTTPException(status_code=404, detail={"item id not found!"}) 
    return hero

'''Delete a Hero'''
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero: 
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


