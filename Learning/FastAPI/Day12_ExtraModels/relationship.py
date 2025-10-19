from sqlmodel import Field, Relationship, Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_all_db():
    SQLModel.metadata.create_all(engine)

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquaters: str

    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")

def create_heroes():
    with Session(engine) as session: 
        team_preventers = Team(
            name="preventers", 
            headquaters="newzeland",
        )
        team_Z_force = Team(
            name="Z-Force", 
            headquaters="island"
        )

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Shiva Chaudhary", age=20, team=team_preventers
        )
        hero_rusty_man = Hero(
            name="Secret",
            secret_name="Umanga Ghimire",
            age = 11, 
            team=team_Z_force
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)

def main():
    create_all_db()
    create_heroes() 

if __name__ == "__main__":
    main()
