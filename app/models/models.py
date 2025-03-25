from __future__ import annotations
from typing import Union
from pydantic import BaseModel, typing, EmailStr
from sqlmodel import Field, SQLModel


class UserData(SQLModel, table=True):
    id: typing.Union[int, None] = Field(default=None, primary_key=True)
    email: str
    first_name: str
    last_name: str
    avatar: str

class UserUpdate(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None

class UserResponse(BaseModel):
    data: UserData


class AppStatus(BaseModel):
    users: int = 0  # Значение по умолчанию
    database: bool


