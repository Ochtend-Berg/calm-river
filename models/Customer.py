# ------------------------------------------------------------------------------------------------------------------------------------------ #

from bootstrap import app, db
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Customer(db.Model, UserMixin):

    # -- TABLE NAME -- #
    __tablename__ = 'customers'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRUCTOR -- #
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

# ------------------------------------------------------------------------------------------------------------------------------------------ #
