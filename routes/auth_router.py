from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import Token, UserLogin, UserRegister, UserResponse
from database import get_db
from utils.token_utils import create_access_token

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_REDIRECT_URL
from service.auth_service import create_user, get_current_user, authenticate_user, authenticate_google

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

@auth_router.post("/", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return db_user

@auth_router.post("/token", response_model=Token)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_login = authenticate_user(db, user)
    if not user_login:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return create_access_token(user_login, timedelta(minutes=2))

@auth_router.get("/google_url")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_CLIENT_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"
    }

@auth_router.get("/google", response_model=Token)
async def auth_google(code: str, db: Session = Depends(get_db)):
    token = authenticate_google(code, db)
    return token

@auth_router.get("/test" ,status_code=200)
def test(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {'User': user}
