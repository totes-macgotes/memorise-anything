from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, RegisterForm

import string
import random

from app_secrets import FLASK_APP_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_APP_SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userdata.db"

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(_id):
    return User.query.filter_by(_id=_id).first()

class User(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String, nullable=False)
	last_name = db.Column(db.String, nullable=False)
	user_email = db.Column(db.String, nullable=False)
	username = db.Column(db.String, unique=True, nullable=False)
	country = db.Column(db.String, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	education_level = db.Column(db.String, nullable=False)
	hashed_password = db.Column(db.String, nullable=False)
	subject_area_want_to_learn = db.Column(db.String, nullable=False)
	how_heard_about_the_project = db.Column(db.String, nullable=False)
	
	def __repr__(self):
		return f"""User '{self.username}'({self._id}):
		first_name: {str(self.first_name)}
		last_name: {str(self.last_name)}
		user_email: {str(self.user_email)}
		username: {str(self.username)}
		country: {str(self.country)}
		age: {str(self.age)}
		education_level: {str(self.education_level)}
		hashed_password: {str(self.hashed_password)}
		subject_area_want_to_learn: {str(self.subject_area_want_to_learn)}
		how_heard_about_the_project: {str(self.how_heard_about_the_project)}
		"""

@app.route("/")
@app.route("/menu")
def menu():
    return "<p>Menu Page</p>"


@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		return redirect(url_for("menu"))

	return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		return redirect(url_for("menu"))

	lower = string.ascii_lowercase
	upper = string.ascii_uppercase
	num = string.digits
	symbols = string.punctuation

	all = lower + upper + num + symbols
	temp = random.sample(all, 12)
	recommended_pw = "".join(temp)


	return render_template("register.html", form=form, recommended_pw=recommended_pw)


if __name__ == "__main__":
	app.run(debug=True)