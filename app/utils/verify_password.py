from passlib.context import CryptContext
from app.config import setting

crypt = CryptContext(schemes=[setting.CRYPT_KEY])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)