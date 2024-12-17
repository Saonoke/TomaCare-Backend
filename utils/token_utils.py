import os
from typing import Annotated
import uuid
from fastapi import HTTPException
from fastapi.params import Depends
from jose import jwt, JWTError
from requests import session

from database.database import get_session
from database.schema import TokenData
from datetime import timedelta, datetime, UTC
from config import SECRET_KEY, JWT_ALG
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select, create_engine

from database.schema.auth_schema import TokenType
from model import IssuedAccessToken, IssuedRefreshToken

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')

def create_access_token(token_data: TokenData, exp_delta: timedelta, device_id: str, session: Session):
    jti = str(uuid.uuid4())
    data = {
        'jti': jti,
        'id': token_data.id,
        'username': token_data.username,
        'type': TokenType.ACCESS.value
    }
    exp = datetime.now(UTC) + exp_delta
    data.update({'exp':exp})
    token = jwt.encode(data, SECRET_KEY, algorithm=JWT_ALG)
    session.add(IssuedAccessToken(
        jti=jti,
        user_id=token_data.id,
        device_id=device_id,
        exp=exp.timestamp(),
        status=True
    ))
    session.commit()
    return token

def clear_exp_issued_token(sess: Session):
    current_ts = int(datetime.now(UTC).timestamp())
    stm = select(IssuedAccessToken).where(IssuedAccessToken.exp < current_ts)
    access_tokens_to_delete = sess.exec(stm).all()
    if access_tokens_to_delete:
        for token in access_tokens_to_delete:
            sess.delete(token)
    stm = select(IssuedRefreshToken).where(IssuedRefreshToken.exp < current_ts)
    refresh_tokens_to_delete = sess.exec(stm).all()
    if refresh_tokens_to_delete:
        for token in refresh_tokens_to_delete:
            sess.delete(token)
    sess.commit()

def is_login(sess: Session, jti: str) -> bool:
    token: IssuedAccessToken|None = sess.get(IssuedAccessToken, jti)
    if token and token.status:
        return True
    return False

def create_refresh_token(token_data: TokenData, exp_delta: timedelta, device_id: str, sess: Session):
    jti = str(uuid.uuid4())
    data = {
        'jti': jti,
        'user_id': token_data.id,
        'type': TokenType.REFRESH.value
    }
    exp = datetime.now(UTC) + exp_delta
    data.update({'exp':exp})
    token = jwt.encode(data, SECRET_KEY, algorithm=JWT_ALG)

    sess.add(IssuedRefreshToken(
        jti=jti,
        user_id=token_data.id,
        device_id=device_id,
        exp=exp.timestamp(),
        revoked=False
    ))
    sess.commit()
    return token

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=JWT_ALG)
    except JWTError as e:
        raise JWTError(e)
