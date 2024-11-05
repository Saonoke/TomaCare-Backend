import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
EXPIRATION_TIME = os.getenv("EXPIRATION_TIME")
JWT_ALG = 'HS256'

# Google API Creds
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_REDIRECT_URL = os.getenv("GOOGLE_CLIENT_REDIRECT_URL")