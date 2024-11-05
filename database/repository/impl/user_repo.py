from sqlmodel import select, Session

from database.repository.meta import UserRepositoryMeta
from model import Users
from database import engine

class UserRepository(UserRepositoryMeta):
    def __init__(self, session:Session):
        self.session = session
        

    def get_by_email(self, _email: str ) -> Users:
        stm = select(Users).where(Users.email == _email)
        result = self.session.exec(stm)
        res = result.first()
        if res is None:
            return False
        return res

    def get_by_username(self, _username: str ) -> Users:
        stm = select(Users).where(Users.username == _username)
        result = self.session.exec(stm)
        res = result.first()
        if res is None:
            return False
        return res

    def get_by_id(self, _id: str ) -> Users:
        result = self.session.get(Users, _id)
        return result

    def edit(self, model: Users, _id: str ) -> Users:
        
        statement = select(Users).where(Users.id == _id)
        results = self.session.exec(statement)
        db_user = results.one()
        if db_user is None:
            return None
        for var, value in vars(model).items():
            setattr(db_user, var, value) if value else None
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def add(self, model: Users ) -> Users:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model
