# ------------------------------------------------------------------------------------------------------------------------------------------ #

from main import app, db
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Booking(db.Model):

    # -- TABLE NAME -- #
    __tablename__ = 'bookings'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), index=True)
    start = db.Column(db.String, nullable=False, unique=False, index=False, default=datetime.utcnow)
    end = db.Column(db.String, nullable=False, unique=False, index=False, default=datetime.utcnow)
    is_reservation = db.Column(db.Boolean(), default=False, index=True)
    is_paid = db.Column(db.Boolean(), default=False, index=True)
    notes = db.Column(db.Text, nullable=True, index=True)
    order_number = db.Column(db.Integer, index=True)
    created_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRUCTOR -- #
    def __init__(self, room_id, start, end, is_reservation, is_paid, notes, order_number):
        self.room_id = room_id
        self.start = start
        self.end = end
        self.is_reservation = is_reservation
        self.is_paid = is_paid
        self.notes = notes
        self.order_number = order_number

# ------------------------------------------------------------------------------------------------------------------------------------------ #
