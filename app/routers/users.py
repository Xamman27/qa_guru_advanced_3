from http import HTTPStatus
from http.client import HTTPException
from typing import Iterable

from fastapi import APIRouter
from starlette.responses import JSONResponse
from fastapi_pagination import Page, add_pagination, paginate
from app.models.models import AppStatus, UserResponse, UserData, UserUpdate
from app.database import users

router = APIRouter(prefix="/api/users")

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = users.get_user(user_id)

    if not user:
        return JSONResponse(
            status_code=404, content={'message': 'User does not exist'}
        )
    return UserResponse(data=user)

@router.get("/", response_model=Page[UserData])
def get_users() -> Iterable[UserData]:
    user_list = users.get_users()
    return paginate(user_list)

@router.post("/", response_model=None)
def create_user(user_data: UserData):
    return users.create_user(user_data)

@router.patch("/{user_id}", response_model=None)
def update_user(user_id: int, user_data: UserData):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalide user")
    UserUpdate.model_validate(user_data.model_dump())
    return users.update_user(user_id, user_data)


@router.delete("/{user_id}", response_model=None)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalide user")
    users.delete_user(user_id)
    return {"message": "User deleted"}
