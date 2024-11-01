# from sqlalchemy import create_engine
from sqlmodel import create_engine
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

database_url = os.getenv("DATABASE_URL")
if database_url:
    DATABASE_URL = database_url
else:
    raise Exception('DATABASE_URL not fount!')

engine = create_engine(DATABASE_URL)