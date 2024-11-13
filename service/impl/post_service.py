from os import set_blocking
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.repository import PostRepository, PostRepositoryMeta, ReactionRepositoryMeta, ReactionRepository
from database.schema import PostInput, PostResponse, ReactionInput
from database.schema.post_schema import ReactionEnum, PostResponseGet
from service.meta import PostServiceMeta
from model import Posts, Users, Reaction


class PostService(PostServiceMeta):

    def __init__(self, session:Session, user: Users = Users()):
        self.session = session
        self._user = user
        self._post_repository : PostRepositoryMeta = PostRepository(self.session)
        self._reaction_repository: ReactionRepositoryMeta = ReactionRepository(self.session)

    def __post_model2schema(self, model: Posts)-> Optional[PostResponse]:
        model_dump = model.model_dump()
        model_dump["count_like"] = len([x for x in model.users_links if str(x.reaction_type) == str(ReactionEnum.LIKE)])
        model_dump["count_dislike"] = len([x for x in model.users_links if str(x.reaction_type) == str(ReactionEnum.DISLIKE)])
        model_dump["liked"] = len([x for x in model.users_links if (x.users_id == self._user.id) and (str(x.reaction_type) == str(ReactionEnum.LIKE))]) == 1
        model_dump["disliked"] = len([x for x in model.users_links if (x.users_id == self._user.id) and (str(x.reaction_type) == str(ReactionEnum.DISLIKE))]) == 1
        return PostResponseGet(**model_dump)

    def get_all(self) -> List[Optional[PostResponse]]:
        posts = self._post_repository.get_all()
        responses = []
        for post in posts:
            responses.append(
                self.__post_model2schema(post)
            )
        return responses

    def get_by_id(self,_id : int) -> PostResponse:
        if not self._post_repository.get_by_id(_id):
            raise HTTPException(status_code=404, detail="ID not found")
        else:
            return self.__post_model2schema(
                self._post_repository.get_by_id(_id)
            )
    
    def get_by_user_id(self, _user_id : int) -> List[Optional[PostResponse]]:
        if not self._post_repository.get_by_user_id(_user_id):
            raise HTTPException(status_code=404, detail="User ID not found")
        else:
            posts = self._post_repository.get_by_user_id(_user_id)
            responses = []
            for post in posts:
                responses.append(
                    self.__post_model2schema(post)
                )
            return responses

    def add(self, post: PostInput) -> PostResponse:
        post = Posts(title=post.title, body=post.body, image_id=post.image_id, user_id=self._user.id)
        return self._post_repository.add(post)

    def edit(self,_post: PostInput,_id: int) -> PostResponse:
        post = self._post_repository.get_by_id(_id)
        if not post:
            raise HTTPException(status_code=404, detail="ID not found")
        if post.user_id != self._user.id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this plant")
        else:
            post = Posts(id= _id,title=_post.title, body=_post.body, image_id=_post.image_id,user_id=self._user.id)
            return self._post_repository.edit(post,_id)

    def delete(self, _id:int) -> bool:
        post = self._post_repository.get_by_id(_id)
        if not post:
            raise HTTPException(status_code=404, detail="ID not found")
        if post.user_id != self._user.id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this plant")
        else :
            return self._post_repository.delete(_id)

    def reaction(self, _post_id: int, _type: ReactionInput) -> bool:
        if not self._post_repository.get_by_id(_post_id):
            raise HTTPException(status_code=404, detail="Posts not found")

        reaction = Reaction(posts_id=_post_id, users_id=self._user.id, reaction_type=_type.type)
        db_react = self._reaction_repository.get(_post_id, self._user.id)

        if not db_react:
            if self._reaction_repository.add(reaction):
                return {
                    'action': _type.type,
                    'success':True
                }
        elif str(db_react.reaction_type) != str(reaction.reaction_type):
            if self._reaction_repository.edit(reaction):
                return {
                    'action': _type.type,
                    'success':True
                }
        elif str(db_react.reaction_type) == str(reaction.reaction_type):
            if self._reaction_repository.delete(_post_id, self._user.id):
                return {
                    'action': 'Remove',
                    'success':True
                }

        return {
            'action': _type.type,
            'success':True
        }

