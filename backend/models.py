import uuid
import joblib
import pandas as pd

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from datetime import date
from pydantic import BaseModel
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier

##test push

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


class BookCancelPredictionHistory(Model):
    cancel_prediction = columns.Boolean(partition_key=True)
    booking_date = columns.Date(primary_key=True, default=date.today)
    id = columns.UUID(primary_key=True)
    probability = columns.Double()
    guest_email = columns.Text()
    room_id = columns.UUID()
    number_of_guest = columns.Integer()
    checkin_date = columns.Date()
    checkout_date = columns.Date()


class BookCancelPredictionModel:
    def __init__(self):
        self.data = pd.read_csv('./dataset/hotel_bookings.csv', delimiter=',')
        self.model_fname_ = 'book_cancel.pkl'

        self.data = self.data.fillna(method='ffill')
        le = preprocessing.LabelEncoder()
        for column in ['hotel', 'arrival_date_month', 'meal', 'country', 'market_segment',
                       'distribution_channel', 'reserved_room_type', 'assigned_room_type',
                       'customer_type', 'reservation_status']:
            le.fit(self.data[column])
            self.data[column] = le.transform(self.data[column])

        try:
            self.model = joblib.load(self.model_fname_)
        except Exception as _:
            self.model = self._train_model()
            joblib.dump(self.model, self.model_fname_)

    def _train_model(self):
        label = self.data['is_canceled'].to_numpy()
        datafeat = self.data[['lead_time', 'arrival_date_month',
                              'arrival_date_day_of_month']].to_numpy()
        model = DecisionTreeClassifier()
        model.fit(datafeat, label)
        return model

    def predict_cancellation(self, lead_time, arrival_date_month, arrival_date_day_of_month):
        data_in = [[lead_time, arrival_date_month, arrival_date_day_of_month]]
        prediction = self.model.predict(data_in)
        probability = self.model.predict_proba(data_in).max()
        return prediction[0].item(), probability.item()
