from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.schema import Token, UserLogin, UserRegister, UserResponse, TokenData
from database import get_db

from utils.token_utils import get_current_user
from controllers.auth_controller import AuthController

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

user_dependency = Annotated[TokenData, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


@auth_router.post("/", response_model=UserResponse)
async def register_user(user: UserRegister, controller: AuthController = Depends(AuthController)):
    return controller.register(user)

@auth_router.post("/token", response_model=Token)
async def login_user(user: UserLogin, controller: AuthController = Depends(AuthController)):
    return controller.login(user)

@auth_router.get("/google-url")
async def login_google(controller: AuthController = Depends(AuthController)):
    return controller.google_url()

@auth_router.get("/google", response_model=Token)
async def auth_google(code: str, controller: AuthController = Depends(AuthController)):
    return controller.google_token(code)

@auth_router.get("/test" ,status_code=200, response_model=TokenData)
async def test(user: user_dependency, controller: AuthController = Depends(AuthController)):
    return controller.userinfo(user)
