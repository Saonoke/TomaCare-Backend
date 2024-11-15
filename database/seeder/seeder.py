from .user_seeder import users_seeder
from .plants_seeder import plants_seeder
from .task_seeder import tasks_seeder
from .post_seeder import PostSeeder
from .reaction_seeder import ReactionSeeder

# from sqlalchemy import create_engine
from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--seed", action='store_true', help = "Add seeder data to database")
parser.add_argument("--reset", action='store_true', help = "Remove seeder data from database")

args = parser.parse_args()

# Load .env file
load_dotenv()

database_url = os.getenv("DATABASE_URL")
if database_url:
    DATABASE_URL = database_url
else:
    raise Exception('DATABASE_URL not found!')


engine = create_engine(DATABASE_URL)

   
def up():
    with Session(engine) as session:
        users_seeder(session).execute()
        plants_seeder(session).execute()
        tasks_seeder(session).execute()
        PostSeeder(session).execute()
        ReactionSeeder(session).execute()


def down():
    with Session(engine) as session:
        ReactionSeeder(session).clear()
        PostSeeder(session).clear()
        tasks_seeder(session).clear()
        plants_seeder(session).clear()
        users_seeder(session).clear()


if __name__ == "__main__":
    if args.seed:
        up()
    if args.reset:
        down()


