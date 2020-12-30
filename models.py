import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from datetime import date
from pydantic import BaseModel


class Room(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()
    hotel_name = columns.Text()
    hotel_location = columns.Text()
    hotel_type = columns.Text()
    guest_capacity = columns.Integer()
    price = columns.Integer()


class RoomBase(BaseModel):
    name: str
    hotel_name: str
    hotel_location: str
    hotel_type: str
    guest_capacity: int
    price: int


class Book(Model):
    guest_email = columns.Text(partition_key=True)
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    booking_date = columns.Date(default=date.today)
    status = columns.Text()
    room_id = columns.UUID()
    number_of_guest = columns.Integer()
    checkin_date = columns.Date()
    checkout_date = columns.Date()


class BookBase(BaseModel):
    guest_email: str
    room_id: uuid.UUID
    number_of_guest: int
    checkin_date: date
    checkout_date: date
