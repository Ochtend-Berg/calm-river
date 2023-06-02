# ------------------------------------------------------------------------------------------------------------------------------------------ #

from models.User import User
from imports import *

# ------------------------------------------------------------------------------------------------------------------------------------------ #

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Log In!')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Usernaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired(), EqualTo('pass_confirm', message='Wachtwoorden moeten overeenkomen!')])
    pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Registreer!')

    def check_email(self, field):
        # Check of het e-mailadres al in de database voorkomt!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')

    def check_username(self, field):
        # Check of de gebruikersnaam nog niet vergeven is!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al vergeven, kies een andere naam!')

class ReviewForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired()], render_kw={"placeholder": "Typ hier uw naam", "class": "form-control"})
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={"placeholder": "Typ hier uw e-mail", "class": "form-control"})
    comment = TextAreaField('Opmerking', render_kw={"placeholder": "Schrijf hier uw bericht.", "class": "form-control"})
    rating_id = SelectField('Beoordeling', choices=[('5', '⭐⭐⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('3', '⭐⭐⭐'), ('2', '⭐⭐'), ('1', '⭐')], validators=[DataRequired()], render_kw={"class": "form-select"})
    submit = SubmitField('Plaats bericht!', render_kw={"class": "btn btn-lg btn-warning mb-5 me-3 text-white"})

# ------------------------------------------------------------------------------------------------------------------------------------------ #
