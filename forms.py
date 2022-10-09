from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo

import os
import pycountry

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.alpha2, country.name) for country in pycountry.countries]

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("login")

class RegisterForm(FlaskForm):
    first_name = StringField("first name", validators=[DataRequired(message="*erforderlich")])
    last_name = StringField("last name", validators=[DataRequired(message="*erforderlich")])
    user_email = StringField("e-mail-address", validators=[DataRequired(message="*erforderlich")])
    username = StringField("username", validators=[DataRequired(message="*erforderlich")])
    country = CountrySelectField("username", validators=[DataRequired(message="*erforderlich")])
    password = PasswordField("password", validators=[DataRequired(message="*erforderlich")])
    confirm_password = PasswordField("confirm password", validators=[DataRequired(message="*erforderlich"), EqualTo("password", message="Das Passwort stimmt nicht überein.")])
    submit = SubmitField("register")