
from typing import Annotated

from sqlmodel import SQLModel, Session, create_engine, Field
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI() 

class student_secret_store(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    username: str | None = Field(index=True)
    password: str

class student_secret(SQLModel):
    username: str | None = Field(index=True)
    password: str

class Connection(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str
    mobile_no: int 
    disabled: bool = Field(default=False)

    user_id : int | None = Field(default=None, foreign_key="student_secret_store.id")

class StudentInfo(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str
    mobile_no: int 
    disabled: bool = Field(default=False)

class create_student_request(SQLModel):
    student_secret: student_secret
    student_info: StudentInfo

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_all_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_all_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/Login")
async def create_username(all_student_info: create_student_request, session: SessionDep):
    student_info = Connection(**all_student_info.student_info.model_dump())
    student_data = student_secret_store(**all_student_info.student_secret.model_dump())

    session.add(student_data)
    session.commit()
    session.refresh(student_data)

    student_info.user_id = student_data.id

    session.add(student_info)
    session.commit()
    session.refresh(student_info)

    return {
        "status": "ok",
        "secret": student_data,
        "info": student_info
    }

