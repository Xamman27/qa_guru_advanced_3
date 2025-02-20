from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from data import users, support_info, user_passwords
from secrets import token_hex
from models.models import *
from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()

@app.get('/api/status', response_model=AppStatus)
def get_status():
    return AppStatus(users=bool(users))


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = users.get(user_id)

    if not user:
        return JSONResponse(
            status_code=404, content={'message': 'User does not exist'}
        )

    return UserResponse(data=user, support=support_info)


@app.get("/api/users/", response_model=Page[UserData])
def get_users():
    user_list = [UserData(**user) for user in users.values()]
    return paginate(user_list)


@app.post("/api/login", response_model=SuccessRegisterData)
def login(user_data: LoginRequest):
    if not user_data.email or not user_data.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")

    user = next((user for user in users.values() if user['email'] == user_data.email), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_passwords.get(user_data.email) != user_data.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    random_token = token_hex(16)
    return SuccessRegisterData(id=user['id'], token=random_token)


add_pagination(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)