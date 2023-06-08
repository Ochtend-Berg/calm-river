from main import db
from imports import *
from flask_login import current_user
from models.User import User
from blueprints.auth.forms import LoginForm
from blueprints.auth.forms import RegistrationForm
from forms import LoginForm, RegistrationForm, ReviewForm

# -- BLUEPRINT('NAME OF BLUEPRINT, NAME OF APPLICATION, FOLDER CONTAINING LOGIC) -- #
auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    active_page = 'my_calm_river'
    form = LoginForm()

    if current_user.is_authenticated:
        flash('Je bent al ingelogd.', 'danger')
        return redirect(url_for('profile_bp.my_profile'), code=302)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Gebruiker bestaat niet.', 'danger')
            return redirect(url_for('login'), code=302)

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Je bent succesvol ingelogd!', 'success')

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('profile_bp.my_profile')
            return redirect(next)
        else:
            flash('U heeft verkeerde gegevens ingevoerd!', 'danger')

    return render_template('login.html', form=form, active_page=active_page)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    active_page = 'my_calm_river'
    form = RegistrationForm()

    if current_user.is_authenticated:
        flash('Je bent nog ingelogd.', 'success')
        return redirect(url_for('profile_bp.my_profile'), code=302)

    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data.lower()).first()
        username = User.query.filter_by(username=form.username.data.lower()).first()

        if email is not None:
            flash('Het gekozen e-mailadres bestaat al!', 'danger')
            return redirect(url_for('auth_bp.register'))

        if username is not None:
            flash('Het gekozen gebruikersnaam bestaat al!', 'danger')
            return redirect(url_for('auth_bp.register'))

        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Dank voor de registratie. Er kan nu ingelogd worden!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form, active_page=active_page)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!', 'danger')
    return redirect(url_for('auth_bp.login'))


if __name__ == '__main__':
    app.run(debug=True)
