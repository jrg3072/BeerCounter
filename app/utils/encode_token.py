from datetime import datetime, timedelta
from jose import jwt
from app.config import setting

def encode_token(username: str):
    token = jwt.encode({"sub": username, "exp": datetime.utcnow() + timedelta(minutes=20)},
                       setting.SECRET_KEY,
                       algorithm=setting.ALGORITHM)
    return token