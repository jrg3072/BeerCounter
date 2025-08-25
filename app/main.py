from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.login import login_router
from app.routers.signup import signup_router
from app.routers.dashboard import dashboard_router

app = FastAPI()
app.include_router(login_router.router)
app.include_router(signup_router.router)
app.include_router(dashboard_router.router)
app.mount("/static", StaticFiles(directory="static"), name="static")