from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import Token, UserLogin, UserRegister, UserResponse, TokenData
from database import get_db

from service.auth_service import get_current_user
from controllers.auth_controller import login, register, google_url, google_token, userinfo

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

user_dependency = Annotated[TokenData, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

@auth_router.post("/", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    return register(user, db)

@auth_router.post("/token", response_model=Token)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return login(user, db)

@auth_router.get("/google-url")
async def login_google():
    return google_url()

@auth_router.get("/google", response_model=Token)
async def auth_google(code: str, db: Session = Depends(get_db)):
    return google_token(code, db)

@auth_router.get("/test" ,status_code=200, response_model=TokenData)
def test(user: user_dependency):
    return userinfo(user)
