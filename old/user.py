

class User:
	current_id = 0 #static attribute

	def __init__(self, first_name, last_name, user_email, username, country, age, education_level, hashed_password, subject_area_want_to_learn, how_heard_about_the_project):
		self._id = self.getNextId()

		self.first_name = first_name
		self.last_name = last_name
		self.user_email = user_email
		self.username = username
		self.country = country
		self.age = age
		self.education_level = education_level
		self.hashed_password = hashed_password
		self.subject_area_want_to_learn = subject_area_want_to_learn
		self.how_heard_about_the_project = how_heard_about_the_project

		'''
		Game data (to be finalised at a later date)
		1. Time played
		2. Time spent on each level
		3. High scores/achievements
		4. Accuracy on each learning point
		'''
	@classmethod
	def getNextId(self):
		this_id = self.current_id
		self.current_id += 1
		return this_id

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



a = User("first_name", "last_name", "user_email", "username", "country", 4, "education_level", "hashed_password", "subject_area_want_to_learn", "how_heard_about_the_project")

b = User("first_name", "last_name", "user_email", "username", "country", 4, "education_level", "hashed_password", "subject_area_want_to_learn", "how_heard_about_the_project")
