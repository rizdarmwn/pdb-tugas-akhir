import db

from typing import Optional
from fastapi import FastAPI

from models import Item, Room, RoomBase, Book, BookBase


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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

# CRUD Book
@app.get("/book")
def get_all_book():
    books = Book.objects().all()
    return {"status_code": 200, "data": list(books)}


@app.get("/book/{book_id}")
def get_book(book_id: str):
    book = Book.get(id=book_id)
    return {"status_code": 200, "data": book}


@app.post("/book")
def create_book(book: BookBase):
    new_book = Book.create(
        guest_email=book.guest_email,
        room_id=book.room_id,
        number_of_guest=book.number_of_guest,
        status="process",
        checkin_date=book.checkin_date,
        checkout_date=book.checkout_date,
    )
    return {"status_code": 200, "data": new_book}


@app.put("/book/{book_id}")
def update_book(book_id: str, book: BookBase):
    updated_book = Book.get(id=book_id).update(
        guest_email=book.guest_email,
        room_id=book.room_id,
        number_of_guest=book.number_of_guest,
        checkin_date=book.checkin_date,
        checkout_date=book.checkout_date,
    )
    return {"status_code": 200, "data": updated_book}


@app.put("/book/{book_id}/status")
def update_book_status(book_id: str, status: str):
    updated_book = Book.get(id=book_id).update(
        status=status
    )
    return {"status_code": 200, "data": updated_book}
