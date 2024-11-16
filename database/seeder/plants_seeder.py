from model import Plants
from sqlmodel import Session, select

class plants_seeder():
    def __init__(self,session:Session):
        self.session = session

    @staticmethod
    def create_plants():
        plants = [
            Plants(id= 1, user_id=1, title="tes",condition="sakit")

            ]
        return plants

    def clear(self):
        plants = self.session.exec(select(Plants)).all()

        for plant in plants :
            self.session.delete(plant)
        self.session.commit()

    def execute(self):
        plants = self.create_plants()

        for plant in plants :
            self.session.add(plant)
        self.session.commit()
