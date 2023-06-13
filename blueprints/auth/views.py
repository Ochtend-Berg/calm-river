from app import db
from app import app
import secrets
import requests
from imports import *
from flask_login import current_user
from flask_mail import Mail, Message
from models.User import User
from blueprints.auth.forms import LoginForm
from blueprints.auth.forms import RegistrationForm, ForgotForm, ResetForm

# -- BLUEPRINT('NAME OF BLUEPRINT, NAME OF APPLICATION, FOLDER CONTAINING LOGIC) -- #
auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    active_page = 'my_calm_river'
    form = LoginForm()

    if current_user.is_authenticated:
        flash('Je bent al ingelogd.', 'danger')
        return redirect(url_for('profile_bp.profile_index'), code=302)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Gebruiker bestaat niet.', 'danger')
            return redirect(url_for('auth_bp.login'), code=302)

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Je bent succesvol ingelogd!', 'success')

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('profile_bp.profile_index')
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
        return redirect(url_for('profile_bp.profile_index'), code=302)

    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data.lower()).first()
        username = User.query.filter_by(username=form.username.data.lower()).first()

        if email is not None:
            flash('Het gekozen e-mailadres bestaat al!', 'danger')
            return redirect(url_for('auth_bp.register'))

        if username is not None:
            flash('Het gekozen gebruikersnaam bestaat al!', 'danger')
            return redirect(url_for('auth_bp.register'))

        user = User(email=form.email.data, username=form.username.data, password=form.password.data, is_admin=0)
        db.session.add(user)
        db.session.commit()

        flash('Dank voor de registratie. Er kan nu ingelogd worden!', 'success')

        return redirect(url_for('auth_bp.login'))

    return render_template('register.html', form=form, active_page=active_page)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!', 'success')
    return redirect(url_for('auth_bp.login'))


mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotForm()
    if form.validate_on_submit():
        email = form.email.data

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Verzend de wachtwoordherstel-e-mail
            token = serializer.dumps(email, salt='password-reset')
            reset_url = url_for('auth_bp.reset_password', token=token, _external=True)

            msg = Message('Wachtwoordherstel', recipients=[email])
            msg.body = f'Klik op de volgende link om uw wachtwoord opnieuw in te stellen: {reset_url}'

            try:
                mail.send(msg)
            except Exception as e:
                flash('Er is een fout opgetreden bij het verzenden van de e-mail. Probeer het later opnieuw.')
                return redirect(url_for('auth_bp.forgot_password'))

            flash('Een e-mail voor wachtwoordherstel is verzonden naar uw adres.', 'success')
            return redirect(url_for('auth_bp.forgot_password'))
        else:
            flash('Dit e-mailadres is niet geregistreerd.', 'danger')

    return render_template('forgot_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except:
        flash('De wachtwoordherstel-link is ongeldig of verlopen.', 'danger')
        return redirect(url_for('auth_bp.forgot_password'))

    form = ResetForm()
    if form.validate_on_submit():
        # Reset het wachtwoord van de gebruiker
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()

            flash('Uw wachtwoord is succesvol gewijzigd.', 'success')
            return redirect(url_for('auth_bp.login'))
        else:
            flash('Er is een fout opgetreden bij het wijzigen van uw wachtwoord. Probeer het later opnieuw.', 'danger')
            return redirect(url_for('auth_bp.forgot_password'))

    return render_template('reset_password.html', form=form)
