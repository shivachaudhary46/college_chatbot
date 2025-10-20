# ====== Important necessary modules ===========
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# ==== create engine =====
engine = create_engine(sqlite_url)

# ===== connect to sqlmodel instances ======
def create_all_db_tables():
    SQLModel.metadata.create_all(engine)

# ====== Create Session ======
def get_session():
    with Session(engine) as session:
        yield session

# ====== Create a Session Dependencies =======
SessionDep = Annotated[Session, Depends(get_session)]

