from typing import Annotated

from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Field, Session, create_engine, SQLModel, select

app = FastAPI()

db_url = "postgresql://postgres:admin@localhost:5432/test"
engine = create_engine(url=db_url, echo=True)


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


@app.on_event("startup")  # noqa
def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/heroes/", response_model=HeroPublic)
async def create_hero(hero: HeroCreate, session: SessionDep):
    print(hero)
    db_hero = Hero.model_validate(hero)
    # print("DB HERO ", db_hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroPublic])
async def get_heroes(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return session.exec(select(Hero).offset(offset).limit(limit)).all()


@app.get("/heroes/{id}", response_model=HeroPublic)
async def get_heroes(id: int, session: SessionDep):  # noqa
    hero = session.get(Hero, id)
    if hero:
        return hero
    raise HTTPException(404, f"User with given id = {id} doesn't exist.")


@app.put("/heroes/{id}", response_model=HeroPublic)
async def update_hero(id: int, hero: HeroUpdate, session: SessionDep): # noqa
    db_hero = session.get(Hero, id)
    if db_hero:
        hero_data = hero.model_dump(exclude_unset=True)
        db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero
    raise HTTPException(404, f"User with given id = {id} doesn't exist.")
