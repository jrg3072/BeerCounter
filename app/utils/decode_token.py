from fastapi import status, HTTPException
from jose import jwt, JWTError
from app.config import setting

def decode_token(token: str):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username = str(payload.get("sub"))
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")