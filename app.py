# ------------------------------------------------------------------------------------------------------------------------------------------ #

from bootstrap import app, db
from imports import *
from models.User import User
from models.Room_type import Room_type
from models.Room import Room
from models.Review import Review
from models.Booking import Booking
from flask import session
import random
from forms import LoginForm, RegistrationForm, ReviewForm
from pprint import pprint


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/')
def home():
    active_page = 'home'
    return render_template('index.html', active_page=active_page)


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/rooms')
def rooms():
    active_page = 'rooms'
    room_types = Room_type.query.all()
    return render_template('rooms/rooms.html', room_types=room_types, active_page=active_page)


@app.route('/rooms/step-1/<slug>', methods=['GET', 'POST'])
def rooms_step1(slug):
    if request.method == 'POST':
        form_data = {}
        form = request.form
        for v in form:
            form_data[v] = request.form[v]

        # DATA STEP 1
        session["form_data"] = form_data
        return redirect(url_for('rooms_step2', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'
        previous_data = session.get('form_data', '')
        get_room_type = Room_type.query.filter_by(slug=slug).first()
        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            get_rooms = Room.query.filter_by(room_type_id=get_room_type.id).all()
            return render_template('rooms/step-1.html', active_page=active_page, get_room_type=get_room_type,
                                   get_rooms=get_rooms, previous_data=previous_data)


@app.route('/rooms/step-2/<slug>', methods=['GET', 'POST'])
def rooms_step2(slug):
    if 'form_data' not in session:
        flash('Er is iets misgegaan. Probeer het opnieuw!', 'danger')
        return redirect(url_for('rooms'), code=302)  # Ga terug naar stap 1 als stap 1 niet is voltooid

    if request.method == 'POST':
        form_data = {}
        form = request.form
        for v in form:
            form_data[v] = request.form[v]

        # DATA STEP 2
        session["form_data_1"] = form_data
        return redirect(url_for('rooms_step3', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'

        # PREVIOUS DATA OF STEP 1
        previous_data = session.get('form_data', '')

        # PREVIOUS DATA OF STEP 2
        previous_data_2 = session.get('form_data_1', '')
        get_room_type = Room_type.query.filter_by(slug=slug).first()
        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            return render_template('rooms/step-2.html', active_page=active_page, previous_data=previous_data,
                                   previous_data_2=previous_data_2)


@app.route('/rooms/step-3/<slug>', methods=['GET', 'POST'])
def rooms_step3(slug):
    if 'form_data_1' not in session:
        flash('Er is iets misgegaan. Probeer het opnieuw!', 'danger')
        return redirect(url_for('rooms'), code=302)  # Ga terug naar stap 1 als stap 1 niet is voltooid

    if request.method == 'POST':
        room_number = request.form['room_number']
        start = request.form['date_start']
        end = request.form['date_end']
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

        try:
            booking = Booking(room_id=get_room.id, start=start, end=end, is_reservation=is_reservation, is_paid=is_paid,
                              notes=notes, order_number=order_number)
        except:
            flash('Er is iets misgegaan. Probeer het opnieuw!', 'danger')
            return redirect(url_for('rooms'), code=302)  # Ga terug naar stap 1 als stap 1 niet is voltooid

        db.session.add(booking)
        db.session.commit()

        form_data = {}
        form = request.form
        form_data["order_number"] = order_number
        for v in form:
            form_data[v] = request.form[v]
        session["form_data_3"] = form_data
        return redirect(url_for('rooms_step4', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'
        get_room_type = Room_type.query.filter_by(slug=slug).first()
        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            session["form_data"] = session.get('form_data', '')
            previous_data = session.get('form_data_1', '')
            return render_template('rooms/step-3.html', active_page=active_page, previous_data=previous_data)


@app.route('/rooms/step-4/<slug>')
def rooms_step4(slug):
    if 'form_data_3' not in session:
        flash('Er is iets misgegaan. Probeer het opnieuw!', 'danger')
        session.clear()
        return redirect(url_for('rooms'), code=302)  # Ga terug naar stap 1 als stap 1 niet is voltooid

    reservation_data = session.get("form_data_3")
    active_page = 'rooms'
    get_room_type = Room_type.query.filter_by(slug=slug).first()
    if get_room_type is None:
        return redirect(url_for('rooms'), code=302)

    session.clear()
    return render_template('rooms/step-4.html', active_page=active_page, reservation_data=reservation_data)


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    active_page = 'reviews'
    reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    form = ReviewForm()

    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        rating_id = request.form['rating_id']
        comment = request.form['comment']

        try:
            review = Review(name=name, email=email, rating_id=rating_id, comment=comment)
        except:
            flash('Er is iets misgegaan. Probeer het opnieuw!', 'danger')
            return redirect(url_for('reviews'), code=302)  # Ga terug naar stap 1 als stap 1 niet is voltooid

        db.session.add(review)
        db.session.commit()

        flash('Dank voor uw recensie.', 'success')

        return redirect(url_for('reviews'))

    return render_template('reviews/index.html', form=form, reviews=reviews, active_page=active_page)


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')


@app.route('/contact')
def contact():
    active_page = 'contact'
    return render_template('contact.html', active_page=active_page)


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/bookings/index')
def bookings_index():
    return render_template('bookings/index.html')


@app.route('/bookings/show')
def bookings_show():
    return render_template('bookings/show.html')


@app.route('/bookings/edit')
def bookings_edit():
    return render_template('bookings/edit.html')


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # GRAB USER FROM USER MODELS TABLE
        user = User.query.filter_by(email=form.email.data).first()
        # CHECK PASSWORD USER
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.')
            # IF USER WAS TRYING TO VIST A PAGE THAT REQUIRES A LOGIN
            # FLASK SAVES THAT URL AS 'NEXT'
            next = request.args.get('next')
            # CHECKS IF URL THAT REQUIRES A LOGIN EXISTS
            # OTHERWISE GO TO WELKOM PAGE
            if next == None or not next[0] == '/':
                next = url_for('welkom')
            return redirect(next)

    return render_template('login.html', form=form)


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Dank voor de registratie. Er kan nu ingelogd worden!')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('home'))


# ------------------------------------------------------------------------------------------------------------------------------------------ #

if __name__ == '__main__':
    app.run(debug=True)

# ------------------------------------------------------------------------------------------------------------------------------------------ #
