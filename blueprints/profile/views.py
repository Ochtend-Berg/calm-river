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
    active_page = 'my_calm_river'
    # if request.method == 'POST':
    #     if 'form1_submit' in request.form:
    #         # Logica voor het verwerken van formulier 1
    #         # ...
    #         return 'Formulier 1 is ingediend!'
    #     elif 'form2_submit' in request.form:
    #         # Logica voor het verwerken van formulier 2
    #         # ...
    #         return 'Formulier 2 is ingediend!'

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
        if end_date > today:
            count_current = count_current + 1
        else:
            count_expired = count_expired + 1

    return render_template('profile_index.html', current_user=current_user,
                           active_page=active_page,
                           count_bookings=count_bookings,
                           count_current=count_current,
                           count_expired=count_expired,
                           most_common_room_id=most_common_room_id,
                           room=room,
                           room_type=room_type)
