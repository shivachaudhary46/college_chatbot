from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session, Field, select

app = FastAPI() 

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    secret_name: str 
    age: int | None = Field(default=None, index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_all_db():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    hero_1 = Hero(name="Shiva Chaudhary", secret_name="Shivey", age=34)
    hero_2 = Hero(name="Chandu Sharma", secret_name="Chandu", age=104)
    hero_3 = Hero(name="Umanga Ghimire", secret_name="Bantha", age=31)
    hero_4 = Hero(name="Jensa Adhikari", secret_name="Thoti", age=40)
    hero_5 = Hero(name="Grishma Bhatt", secret_name="Grishu prishu", age=48)
    hero_6 = Hero(name="Akrisha Adhikari", secret_name="Akrisha", age=21)
    hero_7 = Hero(name="Anjelika Rimal", secret_name="Dande", age=11)
    hero_8 = Hero(name="Jenish Adhikari", secret_name="Jenis", age=8)

    with Session(engine) as session: 
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)
        session.add(hero_8)

        session.commit()

def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)  #.where(Hero.age > 32).offset(1).limit(3)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)

def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Chandu Sharma")
        results = session.exec(statement)
        hero = results.one()
        print("Before Updating Hero: ", hero)

        hero.age = 16
        session.add(hero)
        session.commit()
        session.refresh(hero)

        print("After Updating Hero: ", hero)

def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Grishma Bhatt")  
        results = session.exec(statement)  
        hero = results.first()

        if hero is None: 
            print("Not found the element might be already deleted")  
        print("Hero: ", hero)  

        session.delete(hero)  
        session.commit()  

        print("Deleted hero:", hero)  

        statement = select(Hero).where(Hero.name == "Grishma Bhatt")  
        results = session.exec(statement)  
        hero = results.first()  

        if hero is None:  
            print("There's no hero named Grishma Bhatt")  
    
def main():
    delete_heroes()

if __name__ == "__main__":
    main()