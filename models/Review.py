# ------------------------------------------------------------------------------------------------------------------------------------------ #

from app import app, db
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Review(db.Model):

    # INTERACTION TABLE BETWEEN BOOKINGS AND CUSTOMERS
    __tablename__ = 'reviews'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    rating_id = db.Column(db.Integer, default=5, index=True)
    email = db.Column(db.String(255))
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRUCTOR -- #
    def __init__(self, name, rating_id, email, comment):
        self.name = name
        self.rating_id = rating_id
        self.email = email
        self.comment = comment

# ------------------------------------------------------------------------------------------------------------------------------------------ #
