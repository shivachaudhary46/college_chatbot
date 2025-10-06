'''
Import Annotated 
and secondly import Depends to create dependencies
and third import Session to create session, SQLModel which is an instance of the SQL alchemy 
create engine for the creating the engine which could connect to the database
'''
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

'''
connecting engine with the database 
and one engine is enough for the connection
'''
engine = create_engine(sqlite_url)

'''
This function will connect the SQLModel instances of the alchemy which 
will search for the table and create_all will create database
'''
def create_all_db_tables():
    SQLModel.metadata.create_all(engine)

'''
yield means the function remembers where the session was, and if we 
commit() or refresh session
it will remember and return in the list
'''
def get_session():
    with Session(engine) as session:
        yield session

'''
create session dependencies
'''
SessionDep = Annotated[Session, Depends(get_session)]