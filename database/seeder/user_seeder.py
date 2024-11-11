from model import Users
from sqlmodel import Session, select

class users_seeder():

    def __init__(self,session:Session):
        self.session = session

    def create_user(self):
        user = [Users(id=1,email="krisnagmerz21@gmail.com",username="saonoke",full_name="krisna andika",password="tes")]
        return user
    
    # def clear_user(self):
    #     users = self.session.exec(select(Users)).all()

    #     for user in users :
    #         self.session.delete(user)
    #         self.session.commit()
        
    
    def execute(self):
        # self.clear_user()
        users = self.create_user()
        
        for user in users :
            self.session.add(user)
            self.session.commit()



        








