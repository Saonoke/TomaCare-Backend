from typing import Optional

from sqlmodel import select, Session

from database.repository.meta import CommentRepositoryMeta
from model import Comments


class CommentRepository(CommentRepositoryMeta):
    def __init__(self, session:Session):
        self.session = session

    def get(self, _post_id: int, _comment_id: int) -> Optional[Comments]:
        statement = select(Comments).where(Comments.post_id == _post_id).where(Comments.id == _comment_id)
        db_comment = self.session.exec(statement).first()
        return db_comment
    
    def get_all_comment_in_post(self, _post_id: int) -> list[Comments]:
        statement = select(Comments).where(Comments.post_id == _post_id)
        results = self.session.exec(statement).all()
        return results

    def add(self, model: Comments) -> Comments:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def edit(self, model: Comments) -> Optional[Comments]:
        db_comment = self.get(model.posts_id, model.users_id)
        if not db_comment:
            return None
        db_comment.commentary = model.commentary
        self.session.add(db_comment)
        self.session.commit()
        self.session.refresh(db_comment)
        return db_comment

    def delete(self, _post_id: int,_comment_id :int):
        db_comment = self.get(_post_id, _comment_id)
        if not db_comment:
            return False
        self.session.delete(db_comment)
        self.session.commit()
        return True