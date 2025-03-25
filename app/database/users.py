from __future__ import annotations
from typing import Iterable

from fastapi import HTTPException
from sqlmodel import Session, select
from .engine import engine
from app.models.models import UserData, UserUpdate


def get_user(user_id: int) -> UserData | None:
    with Session(engine) as session:
        return session.get(UserData, user_id)

def get_users() -> Iterable[UserData]:
    with Session(engine) as session:
        statement = select(UserData)
        return session.exec(statement).all()

def create_user(user_data: UserData) -> UserData:
    with Session(engine) as session:
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return user_data


def update_user(user_id: int, user_data: UserData) -> UserData:
    with Session(engine) as session:
        db_user = session.get(UserData, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user = user_data.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(UserData, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()