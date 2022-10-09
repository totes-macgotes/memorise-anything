from flask import Flask, render_template
from forms import LoginForm, RegisterForm

from app_secrets import FLASK_APP_SECRET_KEY

app = Flask(__name__)

app.secret_key = FLASK_APP_SECRET_KEY

@app.route("/")
@app.route("/menu")
def menu():
    return "<p>Menu Page</p>"


@app.route("/login")
def login():
	form = LoginForm()
	return render_template("login.html", form=form)


@app.route("/register")
def register():
	return "login page"


if __name__ == "__main__":
	app.run(debug=True)