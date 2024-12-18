import hashlib

from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError
from sqlmodel import Session
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
import re

from config import RATE_LIMIT_REQUESTS, RATE_LIMIT_DURATION
from database import engine
from database.schema import TokenData
from database.schema.auth_schema import TokenType
from model import Users
from utils.token_utils import decode_token, clear_exp_issued_token, is_login


class RateLimitingMiddleware(BaseHTTPMiddleware):
    # Rate limiting configurations
    RATE_LIMIT_DURATION = timedelta(minutes=RATE_LIMIT_DURATION)
    RATE_LIMIT_REQUESTS = RATE_LIMIT_REQUESTS

    def __init__(self, app):
        super().__init__(app)
        # Dictionary to store request counts for each IP
        self.request_counts = {}

    async def dispatch(self, request, call_next):
        # Get the client's IP address
        client_ip = request.client.host

        # Check if IP is already present in request_counts
        request_count, last_request = self.request_counts.get(client_ip, (0, datetime.min))

        # Calculate the time elapsed since the last request
        elapsed_time = datetime.now() - last_request

        if elapsed_time > self.RATE_LIMIT_DURATION:
            # If the elapsed time is greater than the rate limit duration, reset the count
            request_count = 1
        else:
            if request_count >= self.RATE_LIMIT_REQUESTS:
                # If the request count exceeds the rate limit, return a JSON response with an error message
                return JSONResponse(
                    status_code=429,
                    content={"message": "Rate limit exceeded. Please try again later."}
                )
            request_count += 1

        # Update the request count and last request timestamp for the IP
        self.request_counts[client_ip] = (request_count, datetime.now())

        # Proceed with the request
        response = await call_next(request)
        return response


class AuthMiddleware(BaseHTTPMiddleware):
    _whitelist_endpoints = {
        'GET': [
            r'^/$',
            r'^/docs$',  # /docs
            r'^/openapi\.json$',  # /openapi.json
            r'^/auth/google$',  # /auth/google
            r'^/auth/google-url$',  # /auth/google-url
        ],
        'POST': [
            r'^/auth$',  # /auth
            r'^/auth/token$',  # /auth/token
            r'^/auth/refresh$',  # /auth/token
            r'^/auth/google$',  # /auth/google
        ],
        'PUT': [],
        'PATCH': [],
        'DELETE': []
    }

    def __init__(self, app):
        super().__init__(app)

    @staticmethod
    def __get_clear_token(authorization_header: str):

        if 'Bearer ' not in authorization_header:
            return JSONResponse(content={'detail':'Access-token must have the form "Bearer <TOKEN>"'}, status_code=400)

        return authorization_header.replace('Bearer ', '')

    @staticmethod
    def __get_route(url: str):
        return f"/{url.split('/', maxsplit=3)[-1]}".split('?')[0]

    def __check_whitelist_route(self, request: Request) -> bool:
        """
            Will return True when accessing whitelisted route.
        """
        for pattern in self._whitelist_endpoints[request.method]:
            if re.match(pattern, self.__get_route(str(request.url))):
                return True
        return False

    async def dispatch(self, request, call_next):
        try:
            # Bypass middleware untuk route whitelist
            if self.__check_whitelist_route(request):
                return await call_next(request)

            # Validasi Authorization header
            auth_header = request.headers.get('authorization')
            if not auth_header:
                return JSONResponse(status_code=400, content={'detail': 'Access-token header is not set'})

            # Decode token
            clear_token = self.__get_clear_token(auth_header)
            try:
                payload = decode_token(clear_token)
            except JWTError as e:
                if str(e) == 'Signature has expired.':
                    return JSONResponse(status_code=401, content={'detail': 'Token has expired.'})
                return JSONResponse(status_code=401, content={'detail': 'Invalid token!'})

            # Validasi tipe token
            if payload.get('type') != TokenType.ACCESS.value:
                return JSONResponse(status_code=401, content={'detail': 'Invalid token type!'})

            # Ambil jti dan validasi login status
            jti_access = payload['jti']
            with Session(engine) as session:
                if not is_login(session, jti_access):
                    return JSONResponse(status_code=401, content={'detail': 'Token has expired.'})

                # Hapus token kadaluwarsa
                clear_exp_issued_token(session)

                # Ambil data user
                user = session.get(Users, payload['id'])
                if not user:
                    return JSONResponse(status_code=403, content={'detail': 'User not found.'})

            # Simpan user dan jti di state request
            request.state.user = user
            request.state.jti_access = jti_access

            return await call_next(request)

        except Exception as e:
            print(e)
            return JSONResponse(status_code=500, content={'detail': 'Something went wrong in our end !'})