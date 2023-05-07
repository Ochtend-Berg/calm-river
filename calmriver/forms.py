# ------------------------------------------------------------------------------------------------------------------------------------------ #

from calmriver.models import User
from calmriver.imports import *

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
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    name = StringField('Naam', validators=[DataRequired()], render_kw={"placeholder": "Naam"})
    rating_id = SelectField("Beoordeling:", choices=["Slecht", "Matig", "Voldoende", "Goed", "Uitstekend"])
    comment = TextAreaField("Bericht", render_kw={"placeholder": "Schrijf hier uw bericht."})
    submit = SubmitField('Plaats bericht!')

# ------------------------------------------------------------------------------------------------------------------------------------------ #

