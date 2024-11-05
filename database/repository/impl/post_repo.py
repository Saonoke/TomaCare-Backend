from typing import List, Optional
from sqlmodel import select, Session

from database.repository.meta import PostRepositoryMeta
from model import Posts
from database.database import engine

class PostRepository(PostRepositoryMeta):
    def get_all(self) -> List[Optional[Posts]]:
        with Session(engine) as session:
            statement = select(Posts)
            results = session.exec(statement).all()
        return results
    def get_by_id(self, _id: int) -> Posts:
        with Session(engine) as session:
            result = session.get(Posts, _id)
        return result
    def get_by_user_id(self, _user_id: int) -> List[Optional[Posts]] :
        with Session(engine) as session:
            statement = select(Posts).where(Posts.user_id == _user_id) 
            results = session.exec(statement).all()
        return results
    def add(self, model: Posts) -> Posts:
        with Session(engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)
        return model
    def edit(self, model: Posts, _id: int) -> Posts:
        with Session(engine) as session:
            statement = select(Posts).where(Posts.id == _id)
            results = session.exec(statement)
            db_post = results.one()
            if db_post is None:
                return None

            db_post.title = model.title
            db_post.body = model.body
            db_post.image_id = model.image_id

            session.commit()
            session.refresh(db_post)
            return db_post
    def delete(self, _id: int) -> bool  :
        with Session(engine) as session:
            statement = select(Posts).where(Posts.id == _id)
            results = session.exec(statement)
            db_post = results.one()
            if db_post is None:
                return None
            session.delete(db_post)
            session.commit()
            return True

    
