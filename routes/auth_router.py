from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database.database import get_session
from database.schema import Token, UserLogin, UserRegister, UserResponse, TokenData

from utils.token_utils import get_current_user
from controllers.auth_controller import AuthController

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

user_dependency = Annotated[TokenData, Depends(get_current_user)]

@auth_router.post("", response_model=UserResponse , status_code=201)
async def register_user(user: UserRegister, session:Session = Depends(get_session)):
    controller = AuthController(session)
    data = controller.register(user)    
    return data

@auth_router.post("/token", response_model=Token)
async def login_user(user: UserLogin, session: Session = Depends(get_session)):
    controller = AuthController(session)
    return controller.login(user)

@auth_router.get("/google-url")
async def login_google(session:Session = Depends(get_session)):
    controller = AuthController(session)
    return controller.google_url()

@auth_router.get("/google", response_model=Token)
async def auth_google(code: str, session:Session = Depends(get_session)):
    controller = AuthController(session)
    return controller.google_token(code)

@auth_router.get("/test" ,status_code=200, response_model=TokenData)
async def test(user: user_dependency, session:Session = Depends(get_session)):
    controller = AuthController(session)
    return controller.userinfo(user)
