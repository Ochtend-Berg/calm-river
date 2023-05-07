# ------------------------------------------------------------------------------------------------------------------------------------------ #

from calmriver import app, db
from calmriver.imports import *
from calmriver.models import User, Review
from calmriver.forms import LoginForm, RegistrationForm, ReviewForm

# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/')
def home():
    return render_template('home.html')

# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/kamers')
def kamers():
    return render_template('kamers.html')

@app.route('/kamers/stap1')
def kamers_stap1():
    return render_template('kamers-stap-1.html')

@app.route('/kamers/stap2')
def kamers_stap2():
    return render_template('kamers-stap-2.html')

@app.route('/kamers/stap3')
def kamers_stap3():
    return render_template('kamers-stap-3.html')

@app.route('/kamers/stap4')
def kamers_stap4():
    return render_template('kamers-stap-4.html')

# ------------------------------------------------------------------------------------------------------------------------------------------ #    

@app.route('/recensies/index')
def recensies_index():
    reviews = Review.query.all()
    return render_template('recensies-index.html', reviews=reviews)

@app.route('/recensies/create', methods=['GET', 'POST'])
def recensies_create():

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

        return redirect(url_for('recensies_index'))

    return render_template('recensies-create.html', form=form)

# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/privacy')
def privacy():
    return render_template('footer-privacy.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('footer-disclaimer.html')

@app.route('/contact')
def contact():
    return render_template('footer-contact.html')

# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/boekingen/index')
def boekingen_index():
    return render_template('boekingen-index.html')

@app.route('/boekingen/show')
def boekingen_show():
    return render_template('boekingen-show.html')

@app.route('/boekingen/edit')
def boekingen_edit():
    return render_template('boekingen-edit.html')

# ------------------------------------------------------------------------------------------------------------------------------------------ #

@app.route('/welkom')
@login_required
def welkom():
    return render_template('welkom.html')

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
