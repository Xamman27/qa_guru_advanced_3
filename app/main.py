from fastapi import FastAPI, HTTPException, status
import dotenv
dotenv.load_dotenv()
from fastapi_pagination import Page, add_pagination, paginate
from routers import users, status
import uvicorn
from app.database.engine import create_database


app = FastAPI()
app.include_router(users.router)
app.include_router(status.router)

# @app.post("/api/login", response_model=SuccessRegisterData)
# def login(user_data: LoginRequest):
#     if not user_data.email or not user_data.password:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")
#
#     user = next((user for user in users.values() if user['email'] == user_data.email), None)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#
#     if user_passwords.get(user_data.email) != user_data.password:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
#
#     random_token = token_hex(16)
#     return SuccessRegisterData(id=user['id'], token=random_token)


add_pagination(app)

if __name__ == "__main__":
    create_database()
    uvicorn.run(app, host="0.0.0.0", port=8001)