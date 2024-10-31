from datetime import timedelta
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserLogin, UserRegister, UserResponse, Token, TokenData
from service.auth_service import create_user, authenticate_user, authenticate_google
from utils.token_utils import create_access_token
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_REDIRECT_URL, EXPIRATION_TIME
from model.user_model import User

def register(user: UserRegister, db: Session = Depends(get_db)) -> UserResponse:
    new_user = create_user(db, user)
    return new_user

def login(user: UserLogin, db: Session = Depends(get_db)) -> UserResponse:
    user_login = authenticate_user(db, user)
    if not user_login:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return create_access_token(user_login, timedelta(hours=EXPIRATION_TIME))

def google_url() -> dict[str:str]:
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_CLIENT_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"
    }

def google_token(code: str, db: Session = Depends(get_db)) -> Token:
    token = authenticate_google(code, db)
    return token

def userinfo(user: User, db: Session = Depends(get_db)) -> TokenData:
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return user