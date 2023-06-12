# ------------------------------------------------------------------------------------------------------------------------------------------ #

from models.User import User
from imports import *


# ------------------------------------------------------------------------------------------------------------------------------------------ #

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Ongeldig e-mailadres ingevoerd!')],
                        render_kw={"placeholder": "name@example.com", "class": "form-control"})
    password = PasswordField('Wachtwoord', validators=[DataRequired()],
                             render_kw={"placeholder": "*******", "class": "form-control"})
    submit = SubmitField('Log In!', render_kw={"class": "btn btn-outline-success"})


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Ongeldig e-mailadres ingevoerd!')],
                        render_kw={"placeholder": "name@example.com", "class": "form-control"})
    username = StringField('Usernaam', validators=[DataRequired()],
                           render_kw={"placeholder": "Gebruiker", "class": "form-control"})
    password = PasswordField('Wachtwoord', validators=[DataRequired(),
                                                       EqualTo('pass_confirm',
                                                               message='Wachtwoorden moeten overeenkomen!')],
                             render_kw={"placeholder": "*******", "class": "form-control"})

    pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()],
                                 render_kw={"placeholder": "*******", "class": "form-control"})
    submit = SubmitField('Registreer!', render_kw={"class": "btn btn-outline-success"})

    def check_email(self, field):
        # Check of het e-mailadres al in de database voorkomt!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')

    def check_username(self, field):
        # Check of de gebruikersnaam nog niet vergeven is!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al vergeven, kies een andere naam!')

class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Ongeldig e-mailadres ingevoerd!')],
                        render_kw={"placeholder": "name@example.com", "class": "form-control"})
    # password = PasswordField('Wachtwoord', validators=[DataRequired(),
    #                                                    EqualTo('pass_confirm',
    #                                                            message='Wachtwoorden moeten overeenkomen!')],
    #                          render_kw={"placeholder": "*******", "class": "form-control"})
    #
    # pass_confirm = PasswordField('Bevestig wachtwoord', validators=[DataRequired()],
    #                              render_kw={"placeholder": "*******", "class": "form-control"})
    submit = SubmitField('Verzenden!', render_kw={"class": "btn btn-outline-success"})
# ------------------------------------------------------------------------------------------------------------------------------------------ #
