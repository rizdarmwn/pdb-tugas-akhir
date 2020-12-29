import db

from typing import Optional
from fastapi import FastAPI, Request

from models import Item, Room, RoomBase
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

## kalo mau pake static uncomment line bawah
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# contoh pake templates
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request" : request, "hello" : "Hello World"})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# CRUD Room
@app.get("/room")
def get_all_room():
    return {"status_code": 200, "data": list(Room.objects().all())}

@app.post("/room")
def create_room(room: RoomBase):
    new_room = Room.create(
        name=room.name,
        hotel_name=room.hotel_name,
        hotel_location=room.hotel_location,
        hotel_type=room.hotel_type,
        guest_capacity=room.guest_capacity,
        price=room.price
    )
    return {"status_code": 200, "data": new_room}

@app.get("/room/{room_id}")
def get_room(room_id: str):
    return {"status_code": 200, "data": Room.get(id=room_id)}

@app.delete("/room/{room_id}")
def delete_room(room_id: str):
    Room.get(id=room_id).delete()
    return {"status_code": 200, "data": {}}

@app.put("/room/{room_id}")
def update_room(room_id: str, room: RoomBase):
    updated_room = Room.get(id=room_id).update(
        name=room.name,
        hotel_name=room.hotel_name,
        hotel_location=room.hotel_location,
        hotel_type=room.hotel_type,
        guest_capacity=room.guest_capacity,
        price=room.price
    )
    return {"status_code": 200, "data": updated_room}

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
