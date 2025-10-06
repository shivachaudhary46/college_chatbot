from sqlmodel import create_engine 

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_all_db_tables():
    SQLModel.metadata.create_all(engine)