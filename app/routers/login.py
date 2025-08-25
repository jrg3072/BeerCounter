from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from passlib.context import CryptContext
from app.db.models.UserLogin import UserLogin
from app.utils.search_user import search_user
from app.utils.verify_password import verify_password
from app.utils.encode_token import encode_token
from app.config import setting


login_router = APIRouter()
templates = Jinja2Templates(directory="templates")
crypt = CryptContext(schemes=[setting.CRYPT_KEY])


######################
### REQUESTS 'GET' ###
######################

@login_router.get("/", response_class=RedirectResponse)
async def redirect_login():
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@login_router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request}, status_code=status.HTTP_200_OK)

#######################
### REQUESTS 'POST' ###
#######################

@login_router.post("/login")
async def login_post(user: UserLogin = Depends(UserLogin.login)):
    saved_user = search_user(user.username)
    if not user or not verify_password(user.password, saved_user["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong username or password")
    user_username = saved_user["username"]
    token = encode_token(user_username)
    response = RedirectResponse(url=f"/dashboard/{user_username}", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

