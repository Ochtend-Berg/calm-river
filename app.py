from bootstrap import app, db
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


@app.route('/')
def home():
    active_page = 'home'
    session["url"] = active_page

    return render_template('index.html', active_page=active_page)


@app.route('/rooms')
def rooms():
    active_page = 'rooms'
    session["url"] = active_page
    room_types = Room_type.query.all()
    return render_template('rooms/rooms.html', room_types=room_types, active_page=active_page)


@app.route('/rooms/step-1/<slug>', methods=['GET', 'POST'])
@login_required
def rooms_step1(slug):
    if request.method == 'POST':
        form_data = {}
        form = request.form
        for v in form:
            form_data[v] = request.form[v]

        session["form_data"] = form_data
        return redirect(url_for('rooms_step2', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'
        session["url"] = 'rooms_step1'
        previous_data = session.get('form_data', '')
        get_room_type = Room_type.query.filter_by(slug=slug).first()

        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            get_rooms = Room.query.filter_by(room_type_id=get_room_type.id).all()
            return render_template('rooms/step-1.html', active_page=active_page, get_room_type=get_room_type,
                                   get_rooms=get_rooms, previous_data=previous_data)


@app.route('/rooms/step-2/<slug>', methods=['GET', 'POST'])
@login_required
def rooms_step2(slug):
    if 'form_data' not in session:
        url = session.get('url', 'rooms')
        if url == 'rooms':
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
        return redirect(url_for('rooms_step3', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'
        session["url"] = 'rooms_step2'
        previous_data = session.get('form_data', '')
        previous_data_2 = session.get('form_data_1', '')
        get_room_type = Room_type.query.filter_by(slug=slug).first()

        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            return render_template('rooms/step-2.html', active_page=active_page, previous_data=previous_data,
                                   previous_data_2=previous_data_2)

@app.route('/rooms/step-3/<slug>', methods=['GET', 'POST'])
@login_required
def rooms_step3(slug):
    if 'form_data_1' not in session:
        url = session.get('url', 'rooms')
        if url == 'rooms':
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
        return redirect(url_for('rooms_step4', slug=request.form["room_type"]))

    else:
        active_page = 'rooms'
        session["url"] = 'rooms_step3'

        get_room_type = Room_type.query.filter_by(slug=slug).first()

        if get_room_type is None:
            return redirect(url_for('rooms'), code=302)
        else:
            session["form_data"] = session.get('form_data', '')
            previous_data = session.get('form_data_1', '')
            return render_template('rooms/step-3.html', active_page=active_page, previous_data=previous_data)


@app.route('/rooms/step-4/<slug>')
@login_required
def rooms_step4(slug):
    if 'form_data_3' not in session:
        url = session.get('url', 'rooms')
        if url == 'rooms':
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

    return render_template('rooms/step-4.html', active_page=active_page, reservation_data=reservation_data)


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    active_page = 'reviews'
    session["url"] = active_page
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
            return redirect(url_for('reviews'), code=302)

        db.session.add(review)
        db.session.commit()

        flash('Dank voor uw recensie.', 'success')

        return redirect(url_for('reviews'))

    return render_template('reviews/index.html', form=form, reviews=reviews, active_page=active_page)


@app.route('/privacy')
def privacy():
    active_page = 'privacy'
    session["url"] = active_page

    return render_template('privacy.html')


@app.route('/disclaimer')
def disclaimer():
    active_page = 'disclaimer'
    session["url"] = active_page

    return render_template('disclaimer.html')


@app.route('/contact')
def contact():
    active_page = 'contact'
    session["url"] = active_page

    active_page = 'contact'
    return render_template('contact.html', active_page=active_page)


@app.route('/bookings/index')
def bookings_index():
    return render_template('bookings/index.html')


@app.route('/bookings/show')
def bookings_show():
    return render_template('bookings/show.html')


@app.route('/bookings/edit')
def bookings_edit():
    return render_template('bookings/edit.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    active_page = 'my_calm_river'
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Gebruiker bestaat niet.', 'danger')
            return redirect(url_for('login'), code=302)

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.', 'success')

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('my_profile')
            return redirect(next)
        else:
            flash('U heeft verkeerde gegevens ingevoerd!', 'danger')

    return render_template('auth/login.html', form=form, active_page=active_page)


@app.route('/register', methods=['GET', 'POST'])
def register():
    active_page = 'my_calm_river'
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Dank voor de registratie. Er kan nu ingelogd worden!', 'success')

        return redirect(url_for('login'))

    return render_template('auth/register.html', form=form, active_page=active_page)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!', 'danger')
    return redirect(url_for('login'))


@app.route('/my-profile/index')
@login_required
def my_profile():
    return render_template('profile/index.html')


@app.route('/my-profile/bookings')
@login_required
def my_bookings():
    return render_template('profile/bookings.html')


if __name__ == '__main__':
    app.run(debug=True)
