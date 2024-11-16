from model import Task
from sqlmodel import Session, select

class tasks_seeder():
    def __init__(self,session:Session):
        self.session = session

    @staticmethod
    def create_task():
        tasks= [
            Task(id=1,plant_id=1,title="water"),
            Task(id=2,plant_id=1,title="haha"),
        ]
        return tasks

    def clear(self):
        tasks = self.session.exec(select(Task)).all()

        for task in tasks :
            self.session.delete(task)
        self.session.commit()

    def execute(self):
        tasks = self.create_task()

        for task in tasks :
            self.session.add(task)
        self.session.commit()