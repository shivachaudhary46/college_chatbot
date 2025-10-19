from sqlmodel import SQLModel, Field, Session, create_engine, select

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
    hero_1 = Hero(name="shiva", secret_name="shiva chaudhary")
    hero_2 = Hero(name="umanga", secret_name="umanga ghimire")
    hero_3 = Hero(name="chandan", secret_name="chandan sharma thakur")

    with Session(engine) as session: 
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        print("After adding the heroes in the session: ")
        print("hero_1", hero_1)
        print("hero_2", hero_2)
        print("hero_3", hero_3)

        session.commit()

        print("After commiting to the session: ")
        print("hero_1", hero_1)
        print("hero_2", hero_2)
        print("hero_3", hero_3)


        print("let's look at the hero id's")
        print("hero_1.id", hero_1.id)
        print("hero_2.id", hero_2.id)
        print("hero_3.id", hero_3.id)

        print("let's look at the hero name")
        print("hero_1.name", hero_1.name)
        print("hero_2.name", hero_2.name)
        print("hero_3.name", hero_3.name)
    

        print("After refresshing the heroes in the session: ")
        print("hero_1", hero_1)
        print("hero_2", hero_2)
        print("hero_3", hero_3)

    print("after closing the session: ")
    print("hero_1", hero_1)
    print("hero_2", hero_2)
    print("hero_3", hero_3)

def create_heroes1():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)

        session.commit()


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        heroes = results.one()
        print(heroes)
        # session.exec(select(Hero)).all()

def select_shiva():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "shiva")
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)

        some_hero = Hero(name="dj", secret_name="dj saramvaje")
        print(some_hero.name == "Deadpond")

def select_where():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age >= 35, Hero.age < 40)
        results = session.exec(statement)
        for hero in results:
            print(hero)

def main():
    select_heroes()

if __name__ == "__main__":
    main() 
