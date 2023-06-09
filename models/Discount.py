# ------------------------------------------------------------------------------------------------------------------------------------------ #

from app import app, db
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Discount(db.Model):

    # -- TABLE NAME -- #
    __tablename__ = 'discounts'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    code = db.Column(db.String(50), index=True)
    discount = db.Column(db.Integer, index=True)
    created_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRUCTOR -- #
    def __init__(self, name, code, discount):
        self.name = name
        self.code = code
        self.discount = discount

# ------------------------------------------------------------------------------------------------------------------------------------------ #
