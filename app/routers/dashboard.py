from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, status, HTTPException, Depends, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from passlib.context import CryptContext
import json
from app.db.mongo import user_collection, ranking_collection
from app.utils.decode_token import decode_token
from app.utils.current_user import current_user
from app.config import setting

dashboard_router = APIRouter()
templates = Jinja2Templates(directory="templates")
crypt = CryptContext(schemes=[setting.CRYPT_KEY])


######################
### REQUESTS 'GET' ###
######################

@dashboard_router.get("/dashboard/{user_username}", response_class=HTMLResponse)
async def dashboard_get(request: Request, user: dict = Depends(current_user)):
    user_data = user_collection.find_one({"username": user["username"]})
    ws_url = f"ws://{setting.BACKEND_HOST}:{setting.BACKEND_PORT}"
    last_time = user_data.get("last_beer_time")
    total_beers = user_data.get("beers.total_beers")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "ws_url": ws_url, "last_time": last_time, "total_beers": total_beers}, status_code=status.HTTP_200_OK)

############################
### REQUESTS 'WebSocket' ###
############################

@dashboard_router.websocket("/dashboard/{user_username}")
async def add_delete_beer(websocket: WebSocket, access_token: str = Cookie(None)):
    await websocket.accept()
    username = decode_token(access_token)
    if not username:
        await websocket.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = user_collection.find_one({"username": username})
    if not user:
        await websocket.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    while True:
        try:
            tipo = await websocket.receive_text()
            map_beer_add = {
                        "cl33_add": "cl33",
                        "cl50_add": "cl50",
                        "jarra_caña_add": "jarra_caña"
            }
            map_beer_delete = {
                        "cl33_delete": "cl33",
                        "cl50_delete": "cl50",
                        "jarra_caña_delete": "jarra_caña"
            }
            if tipo in map_beer_add:
                campo = f"beers.{map_beer_add[tipo]}"
                actual_count = user.get("beers", {}).get(map_beer_add[tipo], 0)
                if actual_count >= 0:
                    user_collection.update_one(
                        {"username": username},
                        {"$inc": {campo: 1, "beers.total_beers": 1},
                        "$set": {"last_beer_time": datetime.utcnow()}}
                    )
                    ranking_collection.update_one(
                        {"username": username},
                        {"$inc": {"total_beers": 1}}
                    )
            if tipo in map_beer_delete:
                campo = f"beers.{map_beer_delete[tipo]}"
                actual_count = user.get("beers", {}).get(map_beer_delete[tipo], 0)
                if actual_count > 0:
                    user_collection.update_one(
                        {"username": username},
                        {"$inc": {campo: -1, "beers.total_beers": -1}}
                    )
                    ranking_collection.update_one(
                        {"username": username},
                        {"$inc": {"total_beers": -1}}
                    )
            updated = user_collection.find_one({"username": username})
            new_beers = updated.get("beers", {})
            await websocket.send_text(json.dumps(new_beers))
        except WebSocketDisconnect:
            print(f"{username} desconectado")
            break