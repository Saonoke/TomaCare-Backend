from jose import jwt, JWTError
from schemas import TokenData
from datetime import timedelta, datetime, UTC
from config import SECRET_KEY, JWT_ALG
import requests

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
    if len(token.split('.')) == 3:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALG)
            return payload if payload else None
        except JWTError as e:
            raise JWTError(e)
    else:
        token_info_url = f'https://oauth2.googleapis.com/tokeninfo?access_token={token}'
        response = requests.get(token_info_url)
        access_token = response.json().get("email")
