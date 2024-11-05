from typing import List
from fastapi import Depends
from controllers.base_controller import BaseController
from model import Posts
from database.schema import PostInput,PostResponse
from service.meta import PostServiceMeta
from service.impl import PostService

class  PostController(BaseController):
    _post_service : PostServiceMeta

    def __init__(self, service: PostServiceMeta = Depends(PostService)):
        self._post_service = service
    
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
            print(post_input)
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


