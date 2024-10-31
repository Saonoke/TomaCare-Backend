import requests
import sqlalchemy
from typing import Annotated
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends

from database import get_db
from model import User
from schemas import UserRegister, UserResponse, UserLogin, Token, UserInfoGoogle, TokenData
from utils import get_password_hash, verify_password, decode_access_token
from config import GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_REDIRECT_URL

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')


def create_user(db: Session, user: UserRegister) -> UserResponse:
    try:
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="User with this email already exists.")

        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="User with this username already exists.")

        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, password=hashed_password, username=user.username, full_name=user.full_name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400)

def authenticate_user(db: Session, login_data: UserLogin) -> UserResponse:
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        return False
    if not verify_password(login_data.password, user.password):
        return False
    return user

def registered_email(email: str, db) -> bool:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    return True

def authenticate_google(code: str, db: Session) -> Token:
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_CLIENT_REDIRECT_URL,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")

    user_info = get_user_info(access_token)
    email = user_info.email
    if not registered_email(email, db):
        try:
            username = email.split('@')[0]
            db_user = User(email=user_info.email, password='-', username=username, full_name=user_info.name)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        except sqlalchemy.exc.IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }

def refresh_token(token: str):
    refresh_url = 'https://oauth2.googleapis.com/token'
    data = {
        'client_id' : GOOGLE_CLIENT_ID,
        'client_secret' : GOOGLE_CLIENT_SECRET,
        'refresh_token' : token,
        'grant_type' : 'refresh_token'
    }
    response = requests.post(refresh_url, data=data)

    print(response.json())

def get_user_info(token: str) -> UserInfoGoogle:
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {token}"})
    payload = user_info.json()
    return UserInfoGoogle(**payload)

async def get_current_user(token: Annotated [str, Depends(oauth2_bearer)], db: Session = Depends(get_db)) -> TokenData:
    if len(token.split('.')) == 3:
        try:
            payload = decode_access_token(token)
            user_id = payload.get('id')
            username = payload.get('username')
            if username is None or user_id is None:
                raise HTTPException(status_code=401, detail='Could not validate user.')
            return TokenData(**{
                'id': str(user_id),
                'username': username
            })
        except JWTError as e:
            if str(e) == 'Signature has expired.':
                raise HTTPException(status_code=401, detail=str(e))
        raise HTTPException(status_code=401, detail=f'Could not validate user.')

    else:
        try:
            payload = get_user_info(token)
            email = payload.email
            user = db.query(User).filter(User.email == email).first()
            if email is None:
                raise HTTPException(status_code=401, detail=f'Could not validate user.')
            return TokenData(**{
                'id': str(user.id),
                'username': user.username
            })
        except:
            raise HTTPException(status_code=401, detail=f'Could not validate user.')

