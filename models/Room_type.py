# ------------------------------------------------------------------------------------------------------------------------------------------ #

from main import app, db
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Room_type(db.Model):

    # -- TABLE NAME -- #
    __tablename__ = 'room_types'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    slug = db.Column(db.String(255), index=True)
    max_persons = db.Column(db.Integer, index=True)
    bed_persons = db.Column(db.Integer, index=True)
    has_bath = db.Column(db.Integer, index=True)
    has_wifi = db.Column(db.Integer, index=True)
    price = db.Column(db.Float, index=True)
    description = db.Column(db.Text, index=True)
    created_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRUCTOR -- #
    def __init__(self, name, slug, max_persons, bed_persons, has_bath, has_wifi, price, description):
        self.name = name
        self.slug = slug
        self.max_persons = max_persons
        self.bed_persons = bed_persons
        self.has_bath = has_bath
        self.has_wifi = has_wifi
        self.price = price
        self.description = description

# ------------------------------------------------------------------------------------------------------------------------------------------ #
