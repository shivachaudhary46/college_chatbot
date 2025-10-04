from sqlmodel import SQLModel, Field, create_engine, Session, select

class Team(SQLModel, table=True):
    id: int | None = Field(default = None, primary_key=True)
    name: str = Field(index=True)
    headquaters: str

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    with Session(engine) as session:
        team_wakandaforever = Team(name="Wakanda Forevor", headquaters="Kathmandu")
        team_z_force = Team(name="Z-force", headquaters="Pokhara")

        session.add(team_wakandaforever)
        session.add(team_z_force)

        session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_wakandaforever.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created Hero: ", hero_deadpond)
        print("Created Hero: ", hero_rusty_man)
        print("Created Hero: ", hero_spider_boy)

        # Updating the heroes
        hero_spider_boy.team_id = team_wakandaforever.id
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("updated hero: ", hero_spider_boy)

        # Deleting the heroes
        hero_spider_boy.team_id = None
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("No longer Preventer: ", hero_spider_boy)

def select_heroes():
    with Session(engine) as session:
        statement = select(Hero, Team).where(Hero.team_id == Team.id)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero: ", hero, "Team: ", team)

    # another way 
    ''' 
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team)
        results = session.exec(statement)
        for hero, team in results:
        print("Hero:", hero, "Team: ", team)
    '''

def select_left_outer_join():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero: ", hero, "Team: ", team)

# def select_heroes():
#     with Session(engine) as session: 
#         statement = select(Hero, Team).join(Team).where(Team.name == "Wakanda Forevor")
#         results = session.exec(statement)
#         for hero, team in results:
#             print("Wakanda Forevor Hero: ", hero, "team; ", team)

def main():
    # create_db_and_tables()
    create_heroes()
    # select_heroes()

if __name__ == "__main__":
    main()

