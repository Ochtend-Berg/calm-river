
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
basic_bp = Blueprint('basic_bp', __name__, template_folder='templates')


@basic_bp.route('/')
def home():
    active_page = 'home'
    session["url"] = active_page

    return render_template('index.html', active_page=active_page)
@basic_bp.route('/privacy')
def privacy():
    active_page = 'privacy'
    session["url"] = active_page

    return render_template('privacy.html')


@basic_bp.route('/disclaimer')
def disclaimer():
    active_page = 'disclaimer'
    session["url"] = active_page

    return render_template('disclaimer.html')


@basic_bp.route('/contact')
def contact():
    active_page = 'contact'
    session["url"] = active_page

    active_page = 'contact'
    return render_template('contact.html', active_page=active_page)


