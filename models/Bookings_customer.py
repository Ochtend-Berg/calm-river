# ------------------------------------------------------------------------------------------------------------------------------------------ #

from app import app, db
from imports import *


# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Bookings_customer(db.Model):
    __tablename__ = 'bookings_customers'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True)
    created_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)

    booking = db.relationship('Booking', backref='bookings_customers')
    customer = db.relationship('Customer', backref='bookings_customers')

    def __init__(self, booking_id, user_id, customer_id):
        self.booking_id = booking_id
        self.user_id = user_id
        self.customer_id = customer_id

# ------------------------------------------------------------------------------------------------------------------------------------------ #
