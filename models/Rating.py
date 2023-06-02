# ------------------------------------------------------------------------------------------------------------------------------------------ #

from bootstrap import app, db
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Rating(db.Model):

    # INTERACTION TABLE BETWEEN BOOKINGS AND CUSTOMERS
    __tablename__ = 'ratings'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(50), index=True)
    created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRUCTOR -- #
    def __init__(self, rating):
        self.rating = rating

# ------------------------------------------------------------------------------------------------------------------------------------------ #
