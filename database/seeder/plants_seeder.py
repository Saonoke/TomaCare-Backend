from model import Plants
from sqlmodel import Session

class plants_seeder():
    def __init__(self,session:Session):
        self.session = session

    def create_plants(self):
        plants = [
            Plants(id= 1, user_id=1, title="tes",condition="sakit")
            
            ]
        return plants

    def execute(self):
        plants = self.create_plants()

        for plant in plants :
            self.session.add(plant)
            self.session.commit()
