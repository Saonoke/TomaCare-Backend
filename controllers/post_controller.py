from typing import List
from fastapi import Depends
from sqlmodel import Session
from controllers.base_controller import BaseController
from database.schema.post_schema import ReactionResponse
from model import Posts, Users
from database.schema import PostInput, PostResponse, ReactionInput
from service.meta import PostServiceMeta
from service.impl import PostService

class  PostController(BaseController):
    _post_service : PostServiceMeta

    def __init__(self,session:Session, user: Users = Users()):
        self._post_service : PostServiceMeta = PostService(session, user= user)
    
    def get_all(self) ->List[PostResponse]:
        try: 
            posts = self._post_service.get_all()
            return [PostResponse.model_validate(post) for post in posts]
        except Exception as e:
            return e
    def get_by_id(self,_id : int)-> PostResponse:
        try:
            return self._post_service.get_by_id(_id)
        except Exception as e:
            return self.ise(e)
    def get_by_user_id(self,_user_id : int)-> List[PostResponse]:
        try:
            posts =  self._post_service.get_by_user_id(_user_id)
            return [PostResponse.model_validate(post) for post in posts]
        except Exception as e:
            return self.ise(e)
    def add(self, post_input : PostInput) -> PostResponse: 
        try:
            return self._post_service.add(post_input)
        except Exception as e:
            return self.ise(e)
    def edit(self,post_input : PostInput,_id : int) -> PostResponse :
        try:
            if self._post_service.get_by_id(_id) :
                return self._post_service.edit(post_input,_id)
            else :
                return  self.ise("post not found")
        except Exception as e:
            return self.ise(e)
    def delete(self, _id :int) -> bool:
        try:
            return self._post_service.delete(_id)
        except Exception as e:
            return self.ise(e)

    def reaction(self, _post_id: int, _type: ReactionInput) -> ReactionResponse:
        try:
            return self._post_service.reaction(_post_id, _type)
        except Exception as e:
            return self.ise(e)

