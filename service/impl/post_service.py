from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.repository import PostRepository,PostRepositoryMeta
from database.schema import PostInput,PostResponse
from service.meta import PostServiceMeta
from model import Posts, Users


class PostService(PostServiceMeta):

    def __init__(self, session:Session, user: Users = Users()):
        self.session = session
        self._user = user
        self._post_repository : PostRepositoryMeta = PostRepository(self.session)

    def get_all(self) -> List[Optional[PostResponse]]:
        return self._post_repository.get_all()
        
    def get_by_id(self,_id : int) -> PostResponse:
        if not self._post_repository.get_by_id(_id):
            raise HTTPException(status_code=404, detail="ID not found")
        else :
            return self._post_repository.get_by_id(_id)
    
    def get_by_user_id(self, _user_id : int) -> List[Optional[PostResponse]]:
        if not self._post_repository.get_by_user_id(_user_id):
            raise HTTPException(status_code=404, detail="User ID not found")
        else :
            return self._post_repository.get_by_user_id(_user_id)

    def add(self, post: PostInput) -> PostResponse:
        post = Posts(title=post.title, body=post.body, image_id=post.image_id, user_id=self._user.id)
        return self._post_repository.add(post)

    def edit(self,post: PostInput,_id: int) -> PostResponse:
        post = self._post_repository.get_by_id(_id)
        if not post:
            raise HTTPException(status_code=404, detail="ID not found")
        if post.user_id != self._user.id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this plant")
        else:
            post = Posts(id= _id,title=post.title, body=post.body, image_id=post.image_id,user_id=self._user.id)
            return self._post_repository.edit(post,_id)

    def delete(self, _id:int) -> bool:
        post = self._post_repository.get_by_id(_id)
        if not post:
            raise HTTPException(status_code=404, detail="ID not found")
        if post.user_id != self._user.id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this plant")
        else :
            return self._post_repository.delete(_id)

