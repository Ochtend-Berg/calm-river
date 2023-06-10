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
profile_bp = Blueprint('profile_bp', __name__, template_folder='templates')


@profile_bp.route('/my-profile/index')
@login_required
def my_profile():
    count_bookings = Bookings_customer.query.filter_by(user_id=current_user.id).count()
    count_current = 0
    count_expired = 0

    # Voer een join uit tussen bookings_customer en bookings op basis van de relatie
    query = db.session.query(Bookings_customer, Booking).join(Bookings_customer.booking)

    # Voeg een filter toe op basis van de user_id
    query = query.filter(Bookings_customer.user_id == current_user.id)

    # Haal de gewenste gegevens op uit de database
    results = query.all()

    end_dates = [booking.end for _, booking in results]
    rooms = [booking.room_id for _, booking in results]

    if not rooms:
        most_common_room_id = "-"
        room = "-"
        room_type = "-"
    else:
        most_common_room_id = max(set(rooms), key=rooms.count)
        room = Room.query.filter_by(id=most_common_room_id).first()
        room_type = Room_type.query.filter_by(id=room.room_type_id).first()

    today = date.today().strftime("%Y-%m-%d")

    for end_date in end_dates:
        if end_date < today:
            count_current = count_current + 1
        else:
            count_expired = count_expired + 1

    return render_template('profile_index.html', current_user=current_user,
                           count_bookings=count_bookings,
                           count_current=count_current,
                           count_expired=count_expired,
                           most_common_room_id=most_common_room_id,
                           room=room,
                           room_type=room_type)


@profile_bp.route('/my-profile/bookings', methods=['GET', 'POST'])
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

    return render_template('bookings.html', results=results, today=today)

@profile_bp.route('/my-profile/bookings/show/<slug>', methods=['GET', 'POST'])
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