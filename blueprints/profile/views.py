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


# INDEX AND EDIT ROUTE OF PROFILE
@profile_bp.route('/my-profile/index', methods=['GET', 'POST'])
@login_required
def profile_index():
    active_page = 'my_calm_river'
    if request.method == 'POST':
        confirm_password = request.form['confirm_password']
        user = User.query.filter_by(email=current_user.email).first()

        if user is not None and user.check_password(confirm_password):
            if 'username' in request.form:
                username = request.form['username'].strip()
                if not username:
                    flash('U moet een gebruikersnaam invoeren!', 'danger')
                    return redirect(url_for('profile_bp.profile_index'))

                user.username = username
            elif 'email' in request.form:
                email = request.form['email'].strip()
                if not email:
                    flash('U moet een e-mailadres invoeren!', 'danger')
                    return redirect(url_for('profile_bp.profile_index'))

                user.email = email

            try:
                db.session.commit()
                flash('Gegevens succesvol bijgewerkt!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Er is iets misgegaan. Probeer het later nog eens!', 'danger')
                app.logger.error(str(e))
        else:
            flash('U heeft een foutief wachtwoord ingevoerd!', 'danger')

    count_bookings = Bookings_customer.query.filter_by(user_id=current_user.id).count()

    query = db.session.query(Bookings_customer, Booking).join(Bookings_customer.booking)
    query = query.filter(Bookings_customer.user_id == current_user.id)
    results = query.all()

    room_ids = [booking.room_id for _, booking in results]
    if room_ids:
        most_common_room_id = max(set(room_ids), key=room_ids.count)
        room = Room.query.get(most_common_room_id)
        room_type = Room_type.query.get(room.room_type_id)
    else:
        most_common_room_id = "-"
        room = "-"
        room_type = "-"

    today = date.today().strftime("%Y-%m-%d")
    count_current = sum(1 for _, booking in results if booking.end > today)
    count_expired = sum(1 for _, booking in results if booking.end <= today)

    return render_template('profile_index.html', current_user=current_user,
                           active_page=active_page,
                           count_bookings=count_bookings,
                           count_current=count_current,
                           count_expired=count_expired,
                           most_common_room_id=most_common_room_id,
                           room=room,
                           room_type=room_type)
