from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.repository import PostRepository,PostRepositoryMeta,ImageRepository,ImageRepositoryMeta
from database.schema import PostInput,PostResponse
from service.meta import PostServiceMeta
from model import Posts, Users,Images


class PostService(PostServiceMeta):

    def __init__(self, session:Session, user: Users = Users()):
        self.session = session
        self._user = user
        self._post_repository : PostRepositoryMeta = PostRepository(self.session)
        self._image_repository :ImageRepositoryMeta = ImageRepository(self.session)

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

    def add(self, post: PostInput) -> Optional[PostResponse]:
        try :
            image_id = self._image_repository.create(Images(image_path=post.image_path))
            post = Posts(title=post.title, body=post.body, image_id=image_id, user_id=self._user.id)
            result =self._post_repository.add(post)
            self.session.commit()
            return result
        except Exception as e:
            print(e)
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Create Failed")
        

    def edit(self,post: PostInput,_id: int) -> PostResponse:
        dbpost = self._post_repository.get_by_id(_id)
        if not dbpost:
            raise HTTPException(status_code=404, detail="ID not found")
        if dbpost.user_id != self._user.id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this Post")
        else:
            try :
                image = Images(image_path=post.image_path)
                self._image_repository.edit(dbpost.image_id,image)
                post = Posts(id= _id,title=post.title, body=post.body,user_id=self._user.id)
                result = self._post_repository.edit(post,_id)
                self.session.commit()
                return result
            except Exception as e:
                print(e)
                self.session.rollback()
                raise HTTPException(status_code=400, detail="Update Failed")



    def delete(self, _id:int) -> bool:
        post = self._post_repository.get_by_id(_id)
        if not post:
            raise HTTPException(status_code=404, detail="ID not found")
        if post.user_id != self._user.id:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this Post")
        else :
            return self._post_repository.delete(_id)

