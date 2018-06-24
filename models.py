from app import db
from werkzeug.security import generate_password_hash

# Creates a user class that stores users' information in a table
class Users(db.Model):

	__tablename__ = "users"

	# Column names
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False)
	street = db.Column(db.String, nullable=False)
	city = db.Column(db.String, nullable=False)
	state = db.Column(db.String, nullable=False)
	zipcode = db.Column(db.String, nullable=False)
	country = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	phone = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	urole = db.Column(db.String, nullable=False)
	stripe_id = db.Column(db.String, nullable=False)
	plan = db.Column(db.String, nullable=False)

	# Initialization
	def __init__(
			self,
			username,
			street,
			city,
			state,
			zipcode,
			country,
			email,
			phone,
			password,
			urole,
			stripe_id,
			plan):
				
		self.username = username
		self.street = street
		self.city = city
		self.state = state
		self.zipcode = zipcode
		self.country = country
		self.email = email
		self.phone = phone
		self.password = generate_password_hash(password) 
		self.urole = urole
		self.stripe_id = stripe_id
		self.plan = plan

	def is_authenticated(self):
		return True

	def is_active(self):
        	return True

	def is_anonymous(self):
        	return False

	def get_id(self):
		return str(self.id).encode("utf-8").decode("utf-8")  

	# Handles the format when printing out a User Object
	def __repr__(self):
		return '<name {}'.format(self.username)


class Plans(db.Model):

	__tablename__ = "plans"

	# Column names
	id = db.Column(db.Integer, primary_key=True)
	stripe_id = db.Column(db.String, nullable=False)
	amount = db.Column(db.Integer, primary_key=False)
	description = db.Column(db.String, nullable=False)

	# Initialization
	def __init__(
			self,
			stripe_id,
			amount,
			description):

		self.stripe_id = stripe_id
		self.amount = amount
		self.description = description
