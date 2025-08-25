from app.db.mongo import user_collection

def search_existing_user(username: str) -> bool:
    return user_collection.find_one({"username": username}) is not None