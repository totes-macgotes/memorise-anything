from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from forms import LoginForm, RegisterForm

import string
import random

from app_secrets import FLASK_APP_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_APP_SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userdata.db"

db = SQLAlchemy()
db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
	return User.query.filter_by(id=id).first()

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
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
		return f"""User '{self.username}'({self.id}):
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
@login_required
def menu():
	return  render_template("menu.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return(redirect(url_for("menu")))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=request.form["username"]).first()
		if user:
			if bcrypt.check_password_hash(user.hashed_password, request.form["password"]):
				flash("Successfully logged in", "success")

				if "remember" in request.form:
					login_user(user, remember=True)

				else:
					login_user(user)

				return redirect(url_for("menu"))
			else:
				flash(f"Invalid password for user {request.form['username']}", "danger")

		else:
			flash(f"No existing user named {request.form['username']}", "danger")

	return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit() and request.form["password"] == request.form["confirm_password"]:
		
		pw_hash = bcrypt.generate_password_hash(request.form["password"].encode('utf8')).decode('utf8')

		new_user = User(first_name=request.form["first_name"], 
			last_name=request.form["last_name"], 
			user_email=request.form["user_email"], 
			username=request.form["username"], 
			country=request.form["country"], 
			age=request.form["age"], 
			education_level=request.form["education_level"], 
			hashed_password=pw_hash, 
			subject_area_want_to_learn=request.form["subject_area_want_to_learn"], 
			how_heard_about_the_project=request.form["how_heard_about_the_project"])

		db.session.add(new_user)
		db.session.commit()

		login_user(new_user)
		flash("Successfully registered", "success")

		return redirect(url_for("menu"))

	elif request.method == "POST":
		for fieldName, errorMessages in form.errors.items():
			for err in errorMessages:
				flash(f"{fieldName}: {err}", "danger")

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