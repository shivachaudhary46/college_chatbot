from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

class model(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str 
    password: str

class model_create(SQLModel):
    username: str
    password: str 

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/register/")
async def store_username(model_data: model_create, session: SessionDep) -> model:
    new_model = model.model_validate(model_data)
    session.add(new_model)
    session.commit()
    session.refresh(model)
    return model

@app.get("/register/")
async def look_username(session: SessionDep):
    statement = select(model)
    results = session.exec(statement)
    heroes = results.all()
    return heroes

