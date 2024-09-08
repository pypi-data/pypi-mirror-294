from fastapi import Request

from fastapi import FastAPI
from user_service.users.service.login_service import LoginService
from user_service.users.service.register_service import RegisterService
from user_service.users.model.models import UserTableSchema

app = FastAPI()


@app.get("/api/user/validate/{name}")
async def root(name: str):
    user = LoginService().validate_login(name, email='', password='')
    return {"message": user}

@app.post("/api/user/register")
async def register(user: UserTableSchema):
    if RegisterService().register_user(user):
        return "User registered"

