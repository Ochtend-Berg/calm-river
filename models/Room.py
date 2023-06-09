# ------------------------------------------------------------------------------------------------------------------------------------------ #

from app import app, db
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Room(db.Model):

    # -- TABLE NAME -- #
    __tablename__ = 'rooms'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, index=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'), index=True)
    created_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRUCTOR -- #
    def __init__(self, number, room_type_id):
        self.number = number
        self.room_type_id = room_type_id

# ------------------------------------------------------------------------------------------------------------------------------------------ #
