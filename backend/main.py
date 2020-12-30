import db
import secrets
from fastapi import BackgroundTasks, FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional

from models import Room, RoomBase, Book, BookBase, BookCancelPredictionModel, BookCancelPredictionHistory, User, UserBase

SECRET = "dcb938070508fba2deb38a44aa2024801ca45e5849f6410f"

app = FastAPI()

predict_model = BookCancelPredictionModel()

# kalo mau pake static uncomment line bawah
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

#Auth

#Login manager
# manager = LoginManager(SECRET, tokenUrl='/auth/token', use_cookie=True)

def load_user(email:str, password:str):
    user = User.get(email=email, password=password)
    return user

# # auth token buat login
# @app.route('/auth/token')
# def login(data: OAuth2PasswordRequestForm = Depends()):
#     email = data.username
#     password = data.password

#     user = load_user(email, password)
#     if not user:
#         raise InvalidCredentialsException
#     elif password != user['password']:
#         raise InvalidCredentialsException

#     access_token = manager.create_access_token(
#         data=dict(sub=email)
#     )
#     resp = RedirectResponse(url="/")
#     manager.set_cookie(resp, access_token)
#     return resp
    # return {'access_token' : access_token, 'token_type' : 'bearer'}

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    user = load_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    elif credentials.password != user['password']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# contoh buat login gimana caranya
@app.get("/auth")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}

@app.get('/register')
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request" : request})

@app.post('/register')
def register(user: UserBase):
    new_user = User.create(
        password=user.password,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        gender =  user.gender,
        role = user.role
    )
    return {"status_code" : 200, "data" : new_user}
##END##

# contoh pake templates


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "hello": "Hello World"})

# FRONTEND STARTS


@app.get("/rooms", response_class=HTMLResponse, include_in_schema=False)
def read_room_list(request: Request, user=Depends(get_current_username)):
    return templates.TemplateResponse("list_room.html",  {"request": request, "rooms": list(Room.objects().all())})


@app.get("/bookings", response_class=HTMLResponse, include_in_schema=False)
def read_booking_list(request: Request, user=Depends(get_current_username)):
    return templates.TemplateResponse("list_booking.html",  {"request": request, "bookings": list(Book.objects.all())})


@app.get("/rooms/create", response_class=HTMLResponse, include_in_schema=False)
def create_room_fe(request: Request):
    return templates.TemplateResponse("create_room.html",  {"request": request})



@app.get("/rooms/{room_id}", response_class=HTMLResponse, include_in_schema=False)
def update_room(request: Request, room_id: str, user=Depends(get_current_username)):
    room = Room.get(id=room_id)
    return templates.TemplateResponse("update_room.html",  {"request": request, "room": room})

@app.get("/rooms/{room_id}/book", response_class=HTMLResponse, include_in_schema=False)
def book_room(request: Request, room_id: str, user=Depends(get_current_username)):
    room = Room.get(id=room_id)
    return templates.TemplateResponse("book_room.html",  {"request": request, "room": room})

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
async def create_book(book: BookBase, background_tasks: BackgroundTasks):
    new_book = Book.create(
        guest_email=book.guest_email,
        room_id=book.room_id,
        number_of_guest=book.number_of_guest,
        status="Book",
        checkin_date=book.checkin_date,
        checkout_date=book.checkout_date,
    )
    background_tasks.add_task(predict_book_cancellation, new_book)
    return {"status_code": 200, "data": new_book}


def predict_book_cancellation(book: Book):
    booking_date = book.booking_date.date()
    checkin_date = book.checkin_date.date()

    lead_time = (checkin_date - booking_date).days
    arrival_date_month = checkin_date.month
    arrival_date_day_of_month = checkin_date.day

    prediction, probability = predict_model.predict_cancellation(
        lead_time, arrival_date_month, arrival_date_day_of_month
    )

    BookCancelPredictionHistory.create(
        cancel_prediction=prediction,
        booking_date=booking_date,
        id=book.id,
        probability=probability,
        guest_email=book.guest_email,
        room_id=book.room_id,
        number_of_guest=book.number_of_guest,
        checkin_date=checkin_date,
        checkout_date=book.checkout_date.date()
    )


@app.put("/api/book/{guest_email}/{book_id}/paid")
def checkout_user_book(guest_email: str, book_id: str):
    updated_book = Book.get(guest_email=guest_email, id=book_id).update(
        status="Paid"
    )
    return {"status_code": 200, "data": updated_book}


@app.put("/api/book/{guest_email}/{book_id}/cancel")
def cancel_user_book(guest_email: str, book_id: str):
    updated_book = Book.get(guest_email=guest_email, id=book_id).update(
        status="Canceled"
    )
    return {"status_code": 200, "data": updated_book}


@app.get("/api/cancel-prediction-history")
def history_cancel_prediction():
    predictions = BookCancelPredictionHistory.objects.all()
    return {"status_code": 200, "data": list(predictions)}
