import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from pydantic import BaseModel


class Item(Model):
    id = columns.UUID(primary_key=True)
    name = columns.Text()
    desc = columns.Text()

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
