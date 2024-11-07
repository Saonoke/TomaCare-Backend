from fastapi import FastAPI, Request, Depends, APIRouter
from sqlmodel import Session

from database.database import get_session
from database.schema import  UserResponse
from database.schema.user_schema import UserUpdate, UserChangePassword, UserCreatePassword
# from security.middleware import AuthMiddleware
from controllers import UserController

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@user_router.get("", response_model=UserResponse)
async def get_user(request: Request, session: Session = Depends(get_session)):
    controller = UserController(session)
    return controller.get(request)

@user_router.put("", response_model=UserResponse)
async def update_user(request: Request, user_model: UserUpdate, session: Session = Depends(get_session)):
    controller = UserController(session)
    return controller.update(request, user_model)

@user_router.put("/password", response_model=UserResponse)
async def change_password_user(request: Request, password: UserChangePassword, session: Session = Depends(get_session)):
    controller = UserController(session)
    return controller.change_password(request, password.old_password, password.new_password)

@user_router.post("/password", response_model=UserResponse)
async def create_password_user(request: Request, password: UserCreatePassword, session: Session = Depends(get_session)):
    controller = UserController(session)
    return controller.create_password(request, password.password)