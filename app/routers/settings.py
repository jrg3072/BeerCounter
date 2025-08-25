from fastapi import APIRouter, status, HTTPException, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from app.db.mongo import user_collection, ranking_collection
from app.db.models.UserDelete import UserDelete
from app.utils.verify_password import verify_password
from app.utils.current_user import current_user
from app.config import setting


settings_router = APIRouter()
templates = Jinja2Templates(directory="templates")
crypt = CryptContext(schemes=[setting.CRYPT_KEY])


#########################
### REQUESTS 'DELETE' ###
#########################

@settings_router.post("/settings")
async def delete_user(password: UserDelete = Depends(UserDelete.delete), user: dict = Depends(current_user)):
    check_password = verify_password(password, user["password"])
    if not user or not check_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong username or password")
    user_collection.delete_one({"username": user["username"]})
    ranking_collection.delete_one({"username": user["username"]})
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)