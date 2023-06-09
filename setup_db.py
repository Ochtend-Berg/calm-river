# ------------------------------------------------------------------------------------------------------------------------------------------ #
from app import app, db
from imports import *

with app.app_context():

  # -- IMPORT MODELS -- #
  from models import User
  from models import Customer
  from models import Room_type
  from models import Room
  from models import Discount
  from models import Rate
  from models import Booking
  from models import Bookings_customer
  from models import Review

  db.create_all()

# ------------------------------------------------------------------------------------------------------------------------------------------ #
