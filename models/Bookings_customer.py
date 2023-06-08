# ------------------------------------------------------------------------------------------------------------------------------------------ #

from main import app, db
from imports import *


# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Bookings_customer(db.Model):
    # INTERACTION TABLE BETWEEN BOOKINGS AND CUSTOMERS
    __tablename__ = 'bookings_customers'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True)
    created_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRUCTOR -- #
    def __init__(self, booking_id, user_id, customer_id):
        self.booking_id = booking_id
        self.user_id = user_id
        self.customer_id = customer_id

# ------------------------------------------------------------------------------------------------------------------------------------------ #
