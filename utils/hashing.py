from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(pw_plain: str, pw_hash: str):
    return pwd_context.verify(pw_plain, pw_hash)