from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from jose import jwt, JWTError
from database.schema import TokenData
from datetime import timedelta, datetime, UTC
from config import SECRET_KEY, JWT_ALG
from fastapi.security import OAuth2PasswordBearer

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')

def create_access_token(token_data: TokenData, exp_delta: timedelta):
    data = {
        'id': token_data.id,
        'username': token_data.username
    }
    exp = datetime.now(UTC) + exp_delta
    data.update({'exp':exp})
    token = jwt.encode(data, SECRET_KEY, algorithm=JWT_ALG)

    return {
        'access_token': token,
        'token_type': 'bearer'
    }

def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALG)
        return TokenData(**payload) if payload else None
    except JWTError as e:
        raise JWTError(e)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    try:
        payload = decode_access_token(token)
        user_id = payload.id
        username = payload.username
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