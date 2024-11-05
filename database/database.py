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


def get_session():
    with Session(engine) as session:
        yield session
