from app import app, db
from imports import *
from datetime import date
from sqlalchemy import func
import math
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
bookings_bp = Blueprint('bookings_bp', __name__, template_folder='templates')

@bookings_bp.route('/my-profile/bookings', methods=['GET', 'POST'])
@login_required
def my_bookings():
    today = date.today().strftime("%Y-%m-%d")

    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)

    # Voer een join uit tussen bookings_customer en bookings op basis van de relatie
    query = db.session.query(Bookings_customer, Booking, Room, Room_type).join(Bookings_customer.booking).join(
        Booking.room).join(Room.room_type)

    # Voeg een filter toe op basis van de user_id
    query = query.filter(Bookings_customer.user_id == current_user.id)

    if request.method == 'POST':
        if request.form['filter-selected'] == "0":
            query = query.filter(Booking.order_number == request.form['ordernumber'])

        if request.form['filter'] == 'new':
            query = query.order_by(Booking.created_at.desc())

        if request.form['filter'] == 'old':
            query = query.order_by(Booking.created_at.asc())

        if request.form['filter'] == 'current':
            query = query.filter(Booking.end > today)

            if not query.all():
                flash('Geen resultaten gevonden!', 'danger')
                return redirect(url_for('profile_bp.my_bookings'))

        if request.form['filter'] == 'expired':
            query = query.filter(Booking.end < today)
            query = query.order_by(Booking.created_at.asc())

            if not query.all():
                flash('Geen resultaten gevonden!', 'danger')
                return redirect(url_for('profile_bp.my_bookings'))

        if not query.all() and request.form['filter-selected'] == "0":
            flash('De ordernummer bestaat niet!', 'danger')
            return redirect(url_for('profile_bp.my_bookings'))

    # Haal de gewenste gegevens op uit de database
    results = query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('bookings_index.html', results=results, today=today)

@bookings_bp.route('/my-profile/bookings/show/<slug>', methods=['GET', 'POST'])
@login_required
def my_bookings_show(slug):
    today = date.today().strftime("%Y-%m-%d")

    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)

    # Voer een join uit tussen bookings_customer en bookings op basis van de relatie
    query = db.session.query(Bookings_customer, Customer, Booking, Room, Room_type).join(Bookings_customer.booking).join(Bookings_customer.customer).join(
        Booking.room).join(Room.room_type)

    # Voeg een filter toe op basis van de user_id
    query = query.filter(Bookings_customer.user_id == current_user.id)
    query = query.filter(Booking.order_number == slug)

    if not query.all():
        flash('De boeking bestaat niet!', 'danger')
        return redirect(url_for('profile_bp.my_bookings'))

    # Haal de gewenste gegevens op uit de database
    results = query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('bookings_show.html', results=results, today=today)