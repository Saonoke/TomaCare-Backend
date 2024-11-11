from .user_seeder import users_seeder
from .plants_seeder import plants_seeder
from .task_seeder import tasks_seeder

# from sqlalchemy import create_engine
from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()

database_url = os.getenv("DATABASE_URL")
if database_url:
    DATABASE_URL = database_url
else:
    raise Exception('DATABASE_URL not found!')


engine = create_engine(DATABASE_URL)




   
def main():
    with Session(engine) as session:
        users_seeder(session).execute()
        plants_seeder(session).execute()
        tasks_seeder(session).execute()


if __name__ == "__main__":
    main()


