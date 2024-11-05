from typing import List, Optional
from sqlmodel import select, Session

from database.repository.meta import PostRepositoryMeta
from model import Posts
from database.database import engine

class PostRepository(PostRepositoryMeta):
    def __init__(self,session:Session):
        self.session = session
    def get_all(self) -> List[Optional[Posts]]:
        statement = select(Posts)
        results = self.session.exec(statement).all()
        return results
    def get_by_id(self, _id: int) -> Posts:
        result = self.session.get(Posts, _id)
        return result
    def get_by_user_id(self, _user_id: int) -> List[Optional[Posts]] :
        statement = select(Posts).where(Posts.user_id == _user_id) 
        results = self.session.exec(statement).all()
        return results
    def add(self, model: Posts) -> Posts:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model
    def edit(self, model: Posts, _id: int) -> Posts:
        statement = select(Posts).where(Posts.id == _id)
        results = self.session.exec(statement)
        db_post = results.one()
        if db_post is None:
            return None

        db_post.title = model.title
        db_post.body = model.body
        db_post.image_id = model.image_id

        self.session.commit()
        self.session.refresh(db_post)
        return db_post
    def delete(self, _id: int) -> bool  :
        statement = select(Posts).where(Posts.id == _id)
        results = self.session.exec(statement)
        db_post = results.one()
        if db_post is None:
            return None
        self.session.delete(db_post)
        self.session.commit()
        return True

    
