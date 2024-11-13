from typing import Optional

from sqlmodel import select, Session

from database.repository.meta import ReactionRepositoryMeta
from model import Reaction


class ReactionRepository(ReactionRepositoryMeta):
    def __init__(self, session:Session):
        self.session = session

    def get(self, _post_id: int, _user_id: int) -> Optional[Reaction]:
        statement = select(Reaction).where(Reaction.posts_id == _post_id).where(Reaction.users_id == _user_id)
        db_react = self.session.exec(statement).first()
        return db_react

    def add(self, model: Reaction) -> Reaction:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def edit(self, model: Reaction) -> Optional[Reaction]:
        db_react = self.get(model.posts_id, model.users_id)
        if not db_react:
            return None
        db_react.reaction_type = model.reaction_type
        self.session.add(db_react)
        self.session.commit()
        self.session.refresh(db_react)
        return db_react

    def delete(self, _post_id: int, _user_id: int):
        db_react = self.get(_post_id, _user_id)
        if not db_react:
            return False
        self.session.delete(db_react)
        self.session.commit()
        return True