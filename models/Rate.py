# ------------------------------------------------------------------------------------------------------------------------------------------ #

from main import app, db
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class Rate(db.Model):

    # -- TABLE NAME -- #
    __tablename__ = 'rates'

    # -- TABLE COLUMNS -- #
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, index=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'))
    is_weekend = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False, index=False, default=datetime.utcnow)

    # -- CONSTRAINTS -- #
    __table_args__ = (db.UniqueConstraint('room_type_id', 'is_weekend', name='unique_room_constraint'), None)

    # -- CONSTRUCTOR -- #
    def __init__(self, value, room_type_id, is_weekend):
        self.value = value
        self.room_type_id = room_type_id
        self.is_weekend = is_weekend

# ------------------------------------------------------------------------------------------------------------------------------------------ #
