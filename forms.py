from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField, DateField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo

import os
import pycountry

class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("login")

class RegisterForm(FlaskForm):
    first_name = StringField("first name", validators=[DataRequired(message="*required")])
    last_name = StringField("last name", validators=[DataRequired(message="*required")])
    user_email = StringField("e-mail-address", validators=[DataRequired(message="*required")])
    username = StringField("username", validators=[DataRequired(message="*required")])
    country = CountrySelectField("country", validators=[DataRequired(message="*required")])
    age = SelectField("age", choices=[i for i in range (100)])
    education_level = SelectField("education level", choices=["primary", "secondary (high school)", "university", "post-grad"])
    password = PasswordField("password", validators=[DataRequired(message="*required")])
    confirm_password = PasswordField("confirm password", validators=[DataRequired(message="*required"), EqualTo("password", message="Das Passwort stimmt nicht überein.")])
    subject_area_want_to_learn = TextAreaField("What subject area do you want to learn?", validators=[DataRequired(message="*required")])
    how_heard_about_the_project = TextAreaField("How did you hear about the project?", validators=[DataRequired(message="*required")])
    
    submit = SubmitField("register")