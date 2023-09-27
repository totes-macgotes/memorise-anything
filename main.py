from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from forms import LoginForm, RegisterForm
import card_creator

import string
import random
import pandas as pd
import os
import csv

from app_secrets import FLASK_APP_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_APP_SECRET_KEY

# rules for other pages 
#app.add_url_rule('/dataset_editor', 'd_editor', d_editor, methods=['GET', 'POST'])

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///userdata.db"

db = SQLAlchemy()
db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


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

class Game(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	creator_id = db.Column(db.Integer, nullable=False)
	title = db.Column(db.String, nullable=False)
	
	def __repr__(self):
		return f"""Game '{self.title}'({self.id}):
		creator_id: {str(self.creator_id)}
		title: {str(self.title)}
		"""
	

@app.route("/")
@app.route("/menu")
@login_required
def menu():
	users_games = Game.query.filter_by(creator_id=current_user.id)
	return render_template("menu.html",current_user=current_user, users_games=users_games)


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

@app.route("/gamesetup", methods=["GET", 'POST'])
@login_required
def game_setup():

	display_table = []
	unique_tags = []
	if request.method == "POST":
		if "csv_file" in request.files:
			csv_file = request.files["csv_file"]
			df = pd.read_csv(csv_file)

			display_table = df.values

		elif "game_file" in request.files: 
			game_file = request.files["game_file"]
			#store game file
			game_file.save(os.path.join('static/game_files', game_file.filename))

		else:
			with open('user_datasets/new_dataset.csv', 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				
				# head row 
				writer.writerow(["name", "text_1", "text_2", "image", "sound", "tags"])

				for i in range(int(request.form['entry_count'])):
					name = request.form['name_' + str(i)]
					text_1 = request.form['text_1_' + str(i)]
					text_2 = request.form['text_2_' + str(i)]
					image = request.form['image_' + str(i)]
					sound = request.form['sound_' + str(i)]
					tags = request.form['tags_' + str(i)]
				

					writer.writerow([name, text_1, text_2, image, sound, tags])
					display_table.append([name, text_1, text_2, image, sound, tags])

	# game settings
	if "dataset" in request.files:
		file = request.files['dataset']
		filename = file.filename
		file.save(os.path.join('datasets', filename))

	return render_template("game_setup.html", unique_tags=unique_tags, display_table=display_table, game_files=os.listdir('static/game_files'))

'''
@app.route("/startgame")
@login_required
def start_game():

	if "dataset" in request.files:
		file = request.files['dataset']
		filename = file.filename
		file.save(os.path.join('datasets', filename))

	return render_template("start_game.html")
'''


@app.route("/game", methods=["GET", 'POST'])
@login_required
def game():
	filename = request.files['dataset'].filename
	gamefile =  request.files['dataset']

	if not filename:
		return "no dataset provided"

	
	max_cards = request.form.get('maxcards')
	try:
		int(max_cards)
	except:
		max_cards = 100000

	game_mode_index = int(request.form.get('game_mode'))

	df = pd.read_csv(gamefile)

	df = df.head(int(max_cards))
	
	df2 = pd.DataFrame(columns=df.columns)

	card_creator.clear_dir()

	# text text
	if(game_mode_index == 0):
		for label, row in df.iterrows():
			#label ist zeilennummer 
			if(str(row["text_1"]) == "nan" or str(row["text_2"]) == "nan"):
				continue

			card_creator.create_text_card(str(row["text_1"]), str(label), True)
			card_creator.create_text_card(str(row["text_2"]), str(label), False)

			df2 = pd.concat([df2, pd.DataFrame([row])], ignore_index=True)
			#df2 = df2.append(row, ignore_index=True)

	# text sound
	elif(game_mode_index == 1):
		for label, row in df.iterrows():
			#label ist zeilennummer 
			if(str(row["text_1"]) == "nan" or str(row["sound"]) == "nan"):
				continue

			card_creator.create_text_card(str(row["text_1"]), str(label), True)
		
			df2 = pd.concat([df2, pd.DataFrame([row])], ignore_index=True)
			#df2 = df2.append(row, ignore_index=True)

	# text image
	elif(game_mode_index == 2):
		for label, row in df.iterrows():
			#label ist zeilennummer 
			if(str(row["text_1"]) == "nan" or str(row["image"]) == "nan"):
				continue


			card_creator.create_text_card(str(row["text_1"]), str(label), True)
			card_creator.create_image_card(os.path.join("static/game_files", str(row["image"])), str(label), False)

			df2 = pd.concat([df2, pd.DataFrame([row])], ignore_index=True)
			#df2 = df2.append(row, ignore_index=True)
			
	# random
	elif(game_mode_index == 3):
		for label, row in df.iterrows():
			#label ist zeilennummer 
			if(str(row["text_1"]) == "nan" or str(row["text_2"]) == "nan" or str(row["image"]) == "nan"):
				continue

			card_creator.create_text_card(str(row["text_1"]), str(label), True)
			if random.choice([True, False]):
				card_creator.create_text_card(str(row["text_2"]), str(label), False)
			else:
				card_creator.create_image_card(os.path.join("user_datasets", str(row["image"])), str(label), False)

			df2 = pd.concat([df2, pd.DataFrame([row])], ignore_index=True)
			#df2 = df2.append(row, ignore_index=True)

	print(df2)
	data = df2.to_dict(orient='records')
	return render_template("game_engine/game.html", dataset=data, enumerate=enumerate, str=str, random=random, game_mode_index=game_mode_index)


@app.route("/game_results", methods=['POST', 'GET'])
@login_required
def game_results():
	if request.method == 'GET':
		data = request.args	

	return render_template("game_engine/game_results.html", data=data)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)