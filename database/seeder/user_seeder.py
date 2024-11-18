from model import Users
from sqlmodel import Session, select

from utils import get_password_hash

class users_seeder():

    def __init__(self,session:Session):
        self.session = session

    @staticmethod
    def create_user():
        user = [
            Users(id=1,email="krisnagmerz21@gmail.com",username="saonoke",full_name="krisna andika",password=get_password_hash("tes"),profile_img=1),
            Users(id=2,email="naufalkurniawan605@gmail.com",username="nopal",full_name="Naufal Kurniawan",password=get_password_hash("Admin#1234"),profile_img=1),
            Users(id=3,email="figas@gmail.com",username="figas",full_name="Sofi",password=get_password_hash("Admin#1234"),profile_img=1),
        ]
        return user

    def clear(self):
        users = self.session.exec(select(Users)).all()
        for user in users :
            self.session.delete(user)
        self.session.commit()


    def execute(self):
        users = self.create_user()

        for user in users :
            self.session.add(user)
        self.session.commit()
