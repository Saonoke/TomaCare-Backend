from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(pw_plain: str, pw_hash: str):
    if pw_hash == '-':
        return False
    return pwd_context.verify(pw_plain, pw_hash)

def generate_device_id(user_agent: str, ip_address: str) -> str:
    """
    Generates a unique device ID using a hash of the user agent and IP address.
    """
    raw_data = f"{user_agent}-{ip_address}"
    return hashlib.sha256(raw_data.encode()).hexdigest()