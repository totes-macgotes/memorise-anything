from flask import Flask, render_template, redirect, url_for
from forms import LoginForm, RegisterForm

import string
import random

from app_secrets import FLASK_APP_SECRET_KEY

app = Flask(__name__)

app.secret_key = FLASK_APP_SECRET_KEY

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