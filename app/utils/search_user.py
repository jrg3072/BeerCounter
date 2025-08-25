from fastapi import HTTPException, status
from app.db.mongo import user_collection

def search_user(username: str):
    existing_user = user_collection.find_one({"username": username})
    if existing_user is None:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return dict(**existing_user)