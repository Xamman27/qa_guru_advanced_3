from pydantic import BaseModel


class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class SupportData(BaseModel):
    url: str
    text: str

class UserResponse(BaseModel):
    data: UserData
    support: SupportData

class SuccessRegisterData(BaseModel):
    id: int
    token: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AppStatus(BaseModel):
    users: bool