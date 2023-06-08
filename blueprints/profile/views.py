from main import app, db
from imports import *
from flask_login import current_user
from models.User import User
from models.Room_type import Room_type
from models.Room import Room
from models.Review import Review
from models.Booking import Booking
from models.Bookings_customer import Bookings_customer
from models.Customer import Customer
from flask import session
import random
from forms import LoginForm, RegistrationForm, ReviewForm
from pprint import pprint

# -- BLUEPRINT('NAME OF BLUEPRINT, NAME OF APPLICATION, FOLDER CONTAINING LOGIC) -- #
profile_bp = Blueprint('profile_bp', __name__, template_folder='templates')
@profile_bp.route('/my-profile/index')
@login_required
def my_profile():
    return render_template('profile_index.html')


@profile_bp.route('/my-profile/bookings')
@login_required
def my_bookings():
    return render_template('bookings.html')

