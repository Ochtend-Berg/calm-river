# ------------------------------------------------------------------------------------------------------------------------------------------ #

from calmriver import app, db
from calmriver.imports import *
from calmriver.models import User, Review
from calmriver.forms import LoginForm, RegistrationForm, ReviewForm


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/')
def home():
    active_page = 'home'
    return render_template('index.html', active_page=active_page)


# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/rooms')
def rooms():
    active_page = 'rooms'
    return render_template('rooms/rooms.html', active_page=active_page)


@app.route('/rooms/step-1')
def rooms_step1():
    active_page = 'rooms'
    return render_template('rooms/step-1.html', active_page=active_page)


@app.route('/rooms/step-2')
def rooms_step2():
    active_page = 'rooms'
    return render_template('rooms/step-2.html', active_page=active_page)


@app.route('/rooms/step-3')
def rooms_step3():
    active_page = 'rooms'
    return render_template('rooms/step-3.html', active_page=active_page)


@app.route('/rooms/step-4')
def rooms_step4():
    active_page = 'rooms'
    return render_template('rooms/step-4.html', active_page=active_page)


# ------------------------------------------------------------------------------------------------------------------------------------------ #


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    active_page = 'reviews'
    # User.query.order_by(User.popularity.desc()).limit(10).all()
    reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    form = ReviewForm()

    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        rating_id = request.form['rating_id']
        comment = request.form['comment']

        review = Review(name=name, email=email, rating_id=rating_id, comment=comment)
        db.session.add(review)
        db.session.commit()

        flash('Dank voor uw recensie.')

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
