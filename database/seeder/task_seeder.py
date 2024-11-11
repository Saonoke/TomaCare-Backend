from model import Task
from sqlmodel import Session

class tasks_seeder():
    def __init__(self,session:Session):
        self.session = session

    def create_task(self):
        tasks= [
            Task(id=1,plant_id=1,title="water"),
            Task(id=2,plant_id=1,title="haha"),
        ]

        return tasks
    
    def execute(self):
        tasks = self.create_task()

        for task in tasks :
            self.session.add(task)
            self.session.commit()