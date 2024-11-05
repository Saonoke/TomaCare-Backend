from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError
from sqlmodel import Session
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta

from config import RATE_LIMIT_REQUESTS, RATE_LIMIT_DURATION
from database import engine
from model import Users
from utils.token_utils import decode_access_token

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
    _whitelist_endpoints = [
        '/docs',
        '/openapi.json',
        '/',
        '/auth',
        '/auth/token',
        '/auth/google',
        '/auth/google-url',
    ]

    def __init__(self, app):
        super().__init__(app)

    @staticmethod
    def __get_clear_token(authorization_header: str):

        if 'Bearer ' not in authorization_header:
            return JSONResponse(content={'detail':'Access-token must have the form "Bearer <TOKEN>"'}, status_code=400)

        return authorization_header.replace('Bearer ', '')

    @staticmethod
    def __get_route(url: str):
        return f"/{url.split('/', maxsplit=3)[-1]}"

    def __check_whitelist_route(self, request: Request) -> bool:
        """
            Will return True when accessing whitelisted route.
        """
        if self.__get_route(str(request.url)) in self._whitelist_endpoints:
            return True
        return False

    async def dispatch(self, request, call_next):
        try:
            if self.__check_whitelist_route(request):
                response = await call_next(request)
                return response

            clear_token = self.__get_clear_token(request.headers['authorization'])
            payload = decode_access_token(clear_token)

            with Session(engine) as session:
                user = session.get(Users, payload.id)
        except JWTError as e:
            if str(e) == 'Signature has expired.':
                return JSONResponse(status_code=401, content={'detail': str(e)})
        except Exception as e:
            if str(e) == "'authorization'":
                return JSONResponse(status_code=400, content={
                    'detail': 'Access-token header is not set'
                })
            return JSONResponse(status_code=401, content={'detail':'Could not validate user.'})

        if not user:
            return JSONResponse(content={'detail':'The owner of this access token has not been found'}, status_code=403)

        request.state.user = user
        response = await call_next(request)
        return response