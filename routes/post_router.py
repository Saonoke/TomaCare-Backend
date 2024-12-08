from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from fastapi.params import Query
from sqlmodel import Session
from controllers import PostController
from database.database import get_session
from database.schema import PostInput, PostResponse, ReactionInput
from database.schema.post_schema import ReactionResponse, PostResponseGet,CommentInput,CommentResponse
from model import Reaction

post_router = APIRouter(
    prefix="/post",
    tags=["Post"],
)


@post_router.get("/",response_model=List[PostResponseGet],status_code=200)
async def get_all(
        request: Request,
        search: Optional[str] = Query(None, description="Search by post"),
        limit: Optional[int] = 10,
        session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return  controller.get_all(search=search, limit=limit)

@post_router.get("/{_id}", response_model=PostResponseGet,status_code=200)
async def get_by_id(request: Request, _id : int,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return  controller.get_by_id(_id)

@post_router.get("/user/{_id}",response_model=List[PostResponseGet],status_code=200)
async def get_by_user_id(request: Request, _id : int,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return  controller.get_by_user_id(_id)

@post_router.post("/", response_model=Optional[PostResponse],status_code=201)
async def add(request: Request, postInput : PostInput,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return  controller.add(postInput)

@post_router.put("/{_id}", response_model=Optional[PostResponse],status_code=201)
async def edit(request: Request, postInput : PostInput,_id : int,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return  controller.edit(postInput,_id)

@post_router.delete("/{_id}",status_code=200)
async def delete(request: Request, _id : int,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return   controller.delete(_id)

@post_router.post("/{_id}/reaction", response_model=ReactionResponse, status_code=200)
async def reaction(request: Request, reaction: ReactionInput, _id : int,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return controller.reaction(_id, reaction)

@post_router.post("/{_id}/comment",status_code=200,response_model=PostResponseGet)
async def add_comment(request: Request, _id : int,comment : CommentInput,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return   controller.add_comment(_id,comment)

@post_router.delete("/{_id}/comment/{_comment_id}",status_code=200,response_model=PostResponseGet)
async def del_comment(request: Request, _id : int,_comment_id : int,session:Session = Depends(get_session)):
    controller = PostController(session, user=request.state.user)
    return   controller.del_comment(_id,_comment_id)