# import db

from typing import Optional
from fastapi import FastAPI, Request

from models import Room, RoomBase, Book, BookBase
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# kalo mau pake static uncomment line bawah
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# contoh pake templates


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "hello": "Hello World"})

# FRONTEND STARTS


@app.get("/rooms", response_class=HTMLResponse)
def read_room_list(request: Request):
    return templates.TemplateResponse("list_room.html",  {"request": request})

@app.get("/bookings", response_class=HTMLResponse)
def read_booking_list(request: Request):
    return templates.TemplateResponse("list_booking.html",  {"request": request})

@app.get("/rooms/create", response_class=HTMLResponse)
def create_room_fe(request: Request):
    return templates.TemplateResponse("create_room.html",  {"request": request})

@app.get("/rooms/book", response_class=HTMLResponse)
def book_room(request: Request):
    return templates.TemplateResponse("book_room.html",  {"request": request})


# FRONTEND ENDS

# CRUD Room


@app.get("/api/room")
def get_all_room():
    return {"status_code": 200, "data": list(Room.objects().all())}


@app.post("/api/room")
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


@app.get("/api/room/{room_id}")
def get_room(room_id: str):
    return {"status_code": 200, "data": Room.get(id=room_id)}


@app.delete("/api/room/{room_id}")
def delete_room(room_id: str):
    Room.get(id=room_id).delete()
    return {"status_code": 200, "data": {}}


@app.put("/api/room/{room_id}")
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

# CRUD Book


@app.get("/api/book")
def get_all_book():
    books = list(Book.objects.all())
    return {"status_code": 200, "data": books}


@app.get("/api/books/{guest_email}")
def get_user_book(guest_email: str):
    books = list(Book.filter(guest_email=guest_email))
    return {"status_code": 200, "data": books}


@app.post("/api/book")
def create_book(book: BookBase):
    new_book = Book.create(
        guest_email=book.guest_email,
        room_id=book.room_id,
        number_of_guest=book.number_of_guest,
        status="Booked",
        checkin_date=book.checkin_date,
        checkout_date=book.checkout_date,
    )
    return {"status_code": 200, "data": new_book}


@app.put("/api/book/{guest_email}/{book_id}/checkout")
def checkout_user_book(guest_email: str, book_id: str):
    updated_book = Book.get(guest_email=guest_email, id=book_id).update(
        status="Check-Out"
    )
    return {"status_code": 200, "data": updated_book}


@app.put("/api/book/{guest_email}/{book_id}/cancel")
def cancel_user_book(guest_email: str, book_id: str):
    updated_book = Book.get(guest_email=guest_email, id=book_id).update(
        status="Canceled"
    )
    return {"status_code": 200, "data": updated_book}
