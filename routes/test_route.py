from fastapi import FastAPI, Request

from database.schema import  UserResponse
from security.middleware import AuthMiddleware

user = FastAPI(strip_slashes=False)

user.add_middleware(AuthMiddleware)

@user.get("/", response_model=UserResponse)
async def info_user(request: Request):
    return request.state.user