from sqlmodel import select, Session

from database.repository.meta import UserRepositoryMeta
from model import Users
from database.database import engine

class UserRepository(UserRepositoryMeta):
    def get_by_email(self, _email: str) -> Users:
        stm = select(Users).where(Users.email == _email)
        with Session(engine) as session:
            result = session.exec(stm)
            res = result.first()
        if res is None:
            return False
        return res

    def get_by_username(self, _username: str) -> Users:
        stm = select(Users).where(Users.username == _username)
        with Session(engine) as session:
            result = session.exec(stm)
            res = result.first()
        if res is None:
            return False
        return res

    def get_by_id(self, _id: str) -> Users:
        with Session(engine) as session:
            result = session.get(Users, _id)
        return result

    def edit(self, model: Users, _id: str) -> Users:
        with Session(engine) as session:
            statement = select(Users).where(Users.id == _id)
            results = session.exec(statement)
            db_user = results.one()
            if db_user is None:
                return None

            for var, value in vars(model).items():
                setattr(db_user, var, value) if value else None

            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return

    def add(self, model: Users) -> Users:
        with Session(engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model
