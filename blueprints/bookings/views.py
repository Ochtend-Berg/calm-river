from app import app, db
from imports import *
from datetime import date
from sqlalchemy import func
from sqlalchemy import desc, asc
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

# -- BLUEPRINT('NAME OF BLUEPRINT, NAME OF APPLICATION, FOLDER CONTAINING LOGIC) -- #
bookings_bp = Blueprint('bookings_bp', __name__, template_folder='templates')

ROWS_PER_PAGE = 2


@bookings_bp.route('/my-profile/bookings', methods=['GET', 'POST'])
@login_required
def booking_index():
    active_page = 'my_calm_river'
    today = date.today().strftime("%Y-%m-%d")
    pagination_page = request.args.get('page', 1, type=int)
    page = request.args.get('page', 1, type=int)

    query = db.session.query(Bookings_customer, Booking, Room, Room_type).join(Bookings_customer.booking).join(
        Booking.room).join(Room.room_type)

    if not current_user.is_admin:
        query = query.filter(Bookings_customer.user_id == current_user.id)

    if request.method == 'POST':
        filter_selected = request.form['filter-selected']
        filter_type = request.form['filter']

        if filter_selected == "0":
            query = query.filter(Booking.order_number == request.form['ordernumber'])

        if filter_type == 'new':
            query = query.order_by(desc(Booking.created_at))

        if filter_type == 'old':
            query = query.order_by(asc(Booking.created_at))

        if filter_type == 'current':
            query = query.filter(Booking.end > today)

        if filter_type == 'expired':
            query = query.filter(Booking.end < today).order_by(asc(Booking.created_at))

        results = query.all()

        if not results:
            flash('Geen resultaten gevonden!', 'danger')
            return redirect(url_for('bookings_bp.booking_index'))

        if filter_selected == "0" and not results:
            flash('De ordernummer bestaat niet!', 'danger')
            return redirect(url_for('bookings_bp.booking_index'))

        if pagination_page != 1:
            return redirect(url_for('bookings_bp.booking_index', page=1))

    results = query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('bookings_index.html', results=results, active_page=active_page, today=today)


@bookings_bp.route('/my-profile/bookings/show/<order_number>', methods=['GET', 'POST'])
@login_required
def booking_show(order_number):
    active_page = 'my_calm_river'
    today = date.today().strftime("%Y-%m-%d")
    page = request.args.get('page', 1, type=int)

    query = db.session.query(Bookings_customer, Customer, Booking, Room, Room_type).join(
        Bookings_customer.booking).join(Bookings_customer.customer).join(
        Booking.room).join(Room.room_type)

    if current_user.is_admin == 1:
        query = query.filter(Booking.order_number == order_number)
    elif current_user.is_admin == 0:
        query = query.filter(Bookings_customer.user_id == current_user.id)

    results = query.paginate(page=page, per_page=ROWS_PER_PAGE)

    if not results.items:
        flash('De boeking bestaat niet!', 'danger')
        return redirect(url_for('bookings_bp.booking_index'))

    return render_template('bookings_show.html', active_page=active_page, results=results, today=today)


@bookings_bp.route('/my-profile/bookings/edit/<order_number>', methods=['GET', 'POST'])
@login_required
def booking_edit(order_number):
    active_page = 'my_calm_river'
    today = date.today().strftime("%Y-%m-%d")
    page = request.args.get('page', 1, type=int)

    rooms = db.session.query(Room, Room_type).join(Room.room_type).all()

    query = db.session.query(Bookings_customer, Customer, Booking, Room, Room_type).join(
        Bookings_customer.booking).join(Bookings_customer.customer).join(
        Booking.room).join(Room.room_type)

    if current_user.is_admin == 1:
        query = query.filter(Booking.order_number == order_number)
    elif current_user.is_admin == 0:
        query = query.filter(Bookings_customer.user_id == current_user.id)

    results = query.paginate(page=page, per_page=ROWS_PER_PAGE)

    if not results.items:
        flash('De boeking bestaat niet!', 'danger')
        return redirect(url_for('bookings_bp.booking_index'))

    return render_template('bookings_edit.html', active_page=active_page, rooms=rooms, results=results, today=today)


@bookings_bp.route('/my-profile/bookings/update/<order_number>', methods=['GET', 'POST'])
@login_required
def booking_update(order_number):
    if request.method == 'POST':
        form_data = request.form

        for v in form_data.values():
            if v == "":
                flash('U heeft een leeg veld ingevuld!', 'danger')
                return redirect(url_for('bookings_bp.booking_index'))

        customer_id = form_data['customer_id']
        first_name = form_data['first_name']
        last_name = form_data['last_name']
        email = form_data['email']
        room_id = form_data['room_id']
        start = form_data['date_start']
        end = form_data['date_end']
        notes = form_data['notes']

        customer = Customer.query.get(customer_id)
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
            flash('Boekingsgegevens succesvol bijgewerkt!', 'success')
            return redirect(url_for('bookings_bp.booking_show', order_number=order_number))
        except Exception as e:
            db.session.rollback()
            flash('Er is iets misgegaan. Probeer het later nog eens!', 'danger')
            app.logger.error(str(e))

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

            booking = Booking.query.filter_by(order_number=order_number).first()
            if not booking:
                flash('De boeking bestaat niet!', 'danger')
                return redirect(url_for('bookings_bp.booking_index'))

            try:
                db.session.delete(booking)
                Bookings_customer.query.filter_by(id=booking_customer_id).delete()
                Customer.query.filter_by(id=customer_id).delete()
                db.session.commit()
                flash('Boeking succesvol verwijderd!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Er is iets misgegaan bij het verwijderen van de boeking. Probeer het later nog eens!', 'danger')
                app.logger.error(str(e))

            return redirect(url_for('bookings_bp.booking_index'))
    else:
        return redirect(url_for('bookings_bp.booking_index'))
