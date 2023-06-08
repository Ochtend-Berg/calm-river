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
from pprint import pprint
import random

# -- BLUEPRINT('NAME OF BLUEPRINT, NAME OF APPLICATION, FOLDER CONTAINING LOGIC) -- #
rooms_bp = Blueprint('rooms_bp', __name__, template_folder='templates')

@rooms_bp.route('/index')
def index():
    active_page = 'rooms'
    session["url"] = 'rooms_bp.index'
    room_types = Room_type.query.all()
    return render_template('rooms.html', room_types=room_types, active_page=active_page)
@rooms_bp.route('/step-1/<slug>', methods=['GET', 'POST'])
@login_required
def rooms_step1(slug):
    if request.method == 'POST':
        form_data = {}
        form = request.form
        for v in form:
            form_data[v] = request.form[v]

        session["form_data"] = form_data
        return redirect(url_for('rooms_bp.rooms_step2', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'
        session["url"] = 'rooms_bp.rooms_step1'
        previous_data = session.get('form_data', '')
        get_room_type = Room_type.query.filter_by(slug=slug).first()

        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            get_rooms = Room.query.filter_by(room_type_id=get_room_type.id).all()
            return render_template('step-1.html', active_page=active_page, get_room_type=get_room_type,
                                   get_rooms=get_rooms, previous_data=previous_data)


@rooms_bp.route('/step-2/<slug>', methods=['GET', 'POST'])
@login_required
def rooms_step2(slug):
    if 'form_data' not in session:
        url = session.get('url', 'rooms_bp.index')
        if url == 'rooms_bp.index':
            return redirect(url_for(url), code=302)
        else:
            flash('Vul eerst de gegevens van de huidige stap in!', 'danger')
            return redirect(url_for(url, slug=slug), code=302)

    if request.method == 'POST':
        form_data = {}
        form = request.form
        for v in form:
            form_data[v] = request.form[v]

        session["form_data_1"] = form_data
        return redirect(url_for('rooms_bp.rooms_step3', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'
        session["url"] = 'rooms_bp.rooms_step2'
        previous_data = session.get('form_data', '')
        previous_data_2 = session.get('form_data_1', '')
        get_room_type = Room_type.query.filter_by(slug=slug).first()

        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            return render_template('step-2.html', active_page=active_page, previous_data=previous_data,
                                   previous_data_2=previous_data_2)

@rooms_bp.route('/step-3/<slug>', methods=['GET', 'POST'])
@login_required
def rooms_step3(slug):
    if 'form_data_1' not in session:
        url = session.get('url', 'rooms_bp.index')

        if url == 'rooms_bp.index':
            return redirect(url_for(url), code=302)
        else:
            flash('Vul eerst de gegevens van de huidige stap in!', 'danger')
            return redirect(url_for(url, slug=slug), code=302)

    if request.method == 'POST':
        room_number = request.form['room_number']
        start = request.form['date_start']
        end = request.form['date_end']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        is_reservation = False
        is_paid = False
        notes = request.form['notes']

        order_number_exists = True
        while order_number_exists:
            order_number = random.randint(1000000, 9999999)

            if Booking.query.filter_by(order_number=order_number).count() == 1:
                order_number_exists = True
            else:
                order_number_exists = False

        get_room = Room.query.filter_by(number=room_number).first()

        booking = Booking( room_id=get_room.id, start=start,end=end,is_reservation=is_reservation, is_paid=is_paid, notes=notes, order_number=order_number)

        db.session.add(booking)
        db.session.commit()

        customer = Customer(first_name=first_name, last_name=last_name, email=email)

        db.session.add(customer)
        db.session.commit()

        booking_id = booking.id
        customer_id = customer.id

        booking_customer = Bookings_customer(booking_id=booking_id, user_id=current_user.id, customer_id=customer_id)

        db.session.add(booking_customer)
        db.session.commit()

        form_data = {}
        form = request.form
        form_data["order_number"] = order_number
        for v in form:
            form_data[v] = request.form[v]
        session["form_data_3"] = form_data
        return redirect(url_for('rooms_bp.reservation', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'
        session["url"] = 'rooms_bp.rooms_step3'

        get_room_type = Room_type.query.filter_by(slug=slug).first()

        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            session["form_data"] = session.get('form_data', '')
            previous_data = session.get('form_data_1', '')
            return render_template('step-3.html', active_page=active_page, previous_data=previous_data)


@rooms_bp.route('/reservation/<slug>')
@login_required
def reservation(slug):
    if 'form_data_3' not in session:
        url = session.get('url', 'rooms_bp.index')
        if url == 'rooms_bp.index':
            return redirect(url_for(url), code=302)
        else:
            flash('Vul eerst de gegevens van de huidige stap in!', 'danger')
            return redirect(url_for(url, slug=slug), code=302)

    active_page = 'rooms'
    session["url"] = slug

    reservation_data = session.get("form_data_3")
    get_room_type = Room_type.query.filter_by(slug=slug).first()

    if get_room_type is None:
        return redirect(url_for('rooms'), code=302)

    # VERWIJDERD ALLE FORM DATA
    session.pop('form_data')        # STAP 1
    session.pop('form_data_1')      # STAP 2
    session.pop('form_data_3')      # STAP 3
    session.pop('url')

    return render_template('reservation.html', active_page=active_page, reservation_data=reservation_data)


