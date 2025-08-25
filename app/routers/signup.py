from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from passlib.context import CryptContext
from app.db.mongo import user_collection, ranking_collection
from app.db.models.UserSignup import UserSignup
from app.utils.save_user_ranking import save_user, save_ranking
from app.utils.encode_token import encode_token
from app.utils.search_existing_user import search_existing_user
from app.config import setting


signup_router = APIRouter()
templates = Jinja2Templates(directory="templates")
crypt = CryptContext(schemes=[setting.CRYPT_KEY])


######################
### REQUESTS 'GET' ###
######################

@signup_router.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request}, status_code=status.HTTP_200_OK)

#######################
### REQUESTS 'POST' ###
#######################

@signup_router.post("/signup")
async def signup_post(user: UserSignup = Depends(UserSignup.signup)):
    if search_existing_user(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    hashed_password = crypt.hash(user.password)
    saved_user = save_user(user.username, hashed_password, user.name, user.surname)
    ranking_user = save_ranking(user.username)
    user_collection.insert_one(saved_user)
    ranking_collection.insert_one(ranking_user)
    user_username = user["username"]
    token = encode_token(user_username)
    response = RedirectResponse(url=f"/dashboard/{user_username}", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="strict")
    return response