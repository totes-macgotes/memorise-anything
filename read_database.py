import pycountry

from main import db, User, Game, app


with app.app_context():
	print("Users:")
	[print(x) for x in User.query.all()]
	print("Games:")
	[print(x) for x in Game.query.all()]