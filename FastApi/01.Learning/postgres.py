from typing import Annotated, Sequence

from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, SQLModel, create_engine, Session, select
from pydantic import EmailStr
from fastapi import FastAPI, Depends, Query, Path, HTTPException

from exceptions.CustomExceptions import EmailAlreadyExistsError, UserWithGivenIdDoesntExist

app = FastAPI()


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(index=True, unique=True)


db_url = 'postgresql://postgres:admin@localhost:5432/test'
engine = create_engine(
    url=db_url,
    echo=True
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(user: Users, session: SessionDep) -> Users:
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        raise EmailAlreadyExistsError(409, {f"User with given email : {user.email} already exist!": "Hee"})


@app.get("/heroes/")
def get_all_users(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
) -> Sequence[Users]:
    users = session.exec(select(Users).offset(offset).limit(limit)).all()
    return users


@app.get("/heroes/{id}")
def get_user_with_id(id: Annotated[int,Path(gt=0)],session : SessionDep) -> Users: # noqa
    user = session.get(Users, id)
    if user:
        return user # noqa
    raise UserWithGivenIdDoesntExist(404, f"User with given id doesn't exist = {id}")


@app.delete("/heroes/{id}")
def delete_user(id: Annotated[int,Path(gt=0)], session: SessionDep) -> dict[str,str]: # noqa
    user = session.get(Users, id)
    if user:
        session.delete(user)
        session.commit()
        return {"message": "Delete Success"}
    raise HTTPException(404, f"User with given id doesn't exist = {id}")
