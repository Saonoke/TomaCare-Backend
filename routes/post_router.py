from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from controllers import PostController
from database.database import get_session
from database.schema import  PostInput,PostResponse

post_router = APIRouter(
    prefix="/post",
    tags=["Post"],
)


@post_router.get("/",response_model=List[PostResponse],status_code=200)
async def get_all(session:Session = Depends(get_session)):
    controller = PostController(session)
    return  controller.get_all()

@post_router.get("/{_id}", response_model=PostResponse,status_code=200)
async def get_by_id(_id : int,session:Session = Depends(get_session)):
    controller = PostController(session)
    return  controller.get_by_id(_id)

@post_router.get("/user/{_id}",response_model=List[PostResponse],status_code=200)
async def get_by_user_id(_id : int,session:Session = Depends(get_session)): 
    controller = PostController(session) 
    return  controller.get_by_user_id(_id)

@post_router.post("/", response_model=Optional[PostResponse],status_code=201)
async def add(request: Request, postInput : PostInput,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return  controller.add(postInput)

@post_router.post("/{_id}", response_model=Optional[PostResponse],status_code=201)
async def edit(request: Request, postInput : PostInput,_id : int,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return  controller.edit(postInput,_id)

@post_router.delete("/{_id}",status_code=200)
async def delete(request: Request, _id : int,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return   controller.delete(_id) 