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
def booking_index():
    active_page = 'my_calm_river'
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
                return redirect(url_for('bookings_bp.booking_index'))

        if request.form['filter'] == 'expired':
            query = query.filter(Booking.end < today)
            query = query.order_by(Booking.created_at.asc())

            if not query.all():
                flash('Geen resultaten gevonden!', 'danger')
                return redirect(url_for('bookings_bp.booking_index'))

        if not query.all() and request.form['filter-selected'] == "0":
            flash('De ordernummer bestaat niet!', 'danger')
            return redirect(url_for('bookings_bp.booking_index'))

    # Haal de gewenste gegevens op uit de database
    results = query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('bookings_index.html', results=results, active_page=active_page, today=today)


@bookings_bp.route('/my-profile/bookings/show/<order_number>', methods=['GET', 'POST'])
@login_required
def booking_show(order_number):
    active_page = 'my_calm_river'
    today = date.today().strftime("%Y-%m-%d")

    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)

    # Voer een join uit tussen bookings_customer en bookings op basis van de relatie
    query = db.session.query(Bookings_customer, Customer, Booking, Room, Room_type).join(
        Bookings_customer.booking).join(Bookings_customer.customer).join(
        Booking.room).join(Room.room_type)

    # Voeg een filter toe op basis van de user_id
    query = query.filter(Bookings_customer.user_id == current_user.id)
    query = query.filter(Booking.order_number == order_number)

    if not query.all():
        flash('De boeking bestaat niet!', 'danger')
        return redirect(url_for('bookings_bp.booking_index'))

    # Haal de gewenste gegevens op uit de database
    results = query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('bookings_show.html', active_page=active_page, results=results, today=today)


@bookings_bp.route('/my-profile/bookings/edit/<order_number>', methods=['GET', 'POST'])
@login_required
def booking_edit(order_number):
    active_page = 'my_calm_river'
    today = date.today().strftime("%Y-%m-%d")

    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)

    rooms = db.session.query(Room, Room_type).join(Room.room_type).all()
    pprint(rooms)

    # Voer een join uit tussen bookings_customer en bookings op basis van de relatie
    query = db.session.query(Bookings_customer, Customer, Booking, Room, Room_type).join(
        Bookings_customer.booking).join(Bookings_customer.customer).join(
        Booking.room).join(Room.room_type)

    # Voeg een filter toe op basis van de user_id
    query = query.filter(Bookings_customer.user_id == current_user.id)
    query = query.filter(Booking.order_number == order_number)

    if not query.all():
        flash('De boeking bestaat niet!', 'danger')
        return redirect(url_for('bookings_bp.booking_index'))

    # Haal de gewenste gegevens op uit de database
    results = query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('bookings_edit.html', active_page=active_page, rooms=rooms, results=results, today=today)


@bookings_bp.route('/my-profile/bookings/update/<order_number>', methods=['GET', 'POST'])
@login_required
def booking_update(order_number):
    if request.method == 'POST':
        form_data = {}
        form = request.form
        for v in form:
            if request.form[v] == "":
                flash('U heeft een leeg veld ingevuld!', 'danger')
                return redirect(url_for('bookings_bp.booking_index'))

            form_data[v] = request.form[v]

        order_number = request.form['order_number']
        room_id = request.form['room_id']
        customer_id = request.form['customer_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        start = request.form['date_start']
        end = request.form['date_end']
        notes = request.form['notes']

        customer = Customer.query.filter_by(id=customer_id).first()
        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email

        booking = Booking.query.filter_by(order_number=order_number).first()
        booking.email = email
        booking.room_id = room_id
        booking.start = start
        booking.end = end
        booking.notes = notes

        try:
            db.session.commit()
        except:
            flash('Er is iets misgegaan. Probeer het later nog eens!', 'danger')
            return redirect(url_for('bookings_bp.booking_index'), code=302)

        flash('Boekingsgegevens succesvol bijgewerkt!', 'success')
        return redirect(url_for('bookings_bp.booking_show', order_number=order_number))

    else:
        return redirect(url_for('bookings_bp.booking_index'))


@bookings_bp.route('/my-profile/bookings/delete/<order_number>', methods=['GET', 'POST'])
@login_required
def delete_booking(order_number):
    if request.method == 'POST':
        if current_user.is_admin != 1:
            flash('U bent niet gemachtigd om deze actie uit te voeren!', 'danger')
            return redirect(url_for('bookings_bp.booking_index'))
        else:
            booking_customer_id = request.form['booking_customer_id']
            customer_id = request.form['customer_id']

            booking = Booking.query.filter_by(order_number=order_number).delete()
            if booking is None:
                flash('De boeking bestaat niet!', 'danger')
                return redirect(url_for('bookings_bp.booking_index'))

            Bookings_customer.query.filter_by(id=booking_customer_id).delete()
            Customer.query.filter_by(id=customer_id).delete()

            flash('Boeking succesvol verwijderd!', 'success')
            db.session.commit()

            return redirect(url_for('bookings_bp.booking_index'))
    else:
        return redirect(url_for('bookings_bp.booking_index'))
