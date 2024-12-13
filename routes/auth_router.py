from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from database.database import get_session
from database.schema import Token, UserLogin, UserRegister, UserResponse, TokenData

from controllers.auth_controller import AuthController
from database.schema.auth_schema import RefreshInput, GoogleToken

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("", response_model=UserResponse , status_code=201)
async def register_user(request: Request, user: UserRegister, session:Session = Depends(get_session)):
    controller = AuthController(request, session)
    data = controller.register(user)    
    return data

@auth_router.post("/token", response_model=Token)
async def login_user(request: Request, user: UserLogin, session: Session = Depends(get_session)):
    controller = AuthController(request, session)
    return controller.login(user)

@auth_router.post("/google", response_model=Token)
async def auth_google(request: Request, token: GoogleToken, session:Session = Depends(get_session)):
    controller = AuthController(request, session)
    return controller.google_token(token)

@auth_router.post("/logout")
async def logout(request: Request, session: Session = Depends(get_session)):
    controller = AuthController(request, session)
    return controller.logout(request.state.jti_access)

@auth_router.post("/refresh", response_model=Optional[Token])
async def refresh(request: Request, refresh_token: RefreshInput,session: Session = Depends(get_session)):
    controller = AuthController(request, session)
    return controller.refresh_token(refresh_token)
