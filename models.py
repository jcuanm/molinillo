from app import db
from werkzeug.security import generate_password_hash

# Creates a vendor class that stores vendors' information in a table
class Vendors(db.Model):

	__tablename__ = "vendors"

	# Column names
	id = db.Column(db.Integer, primary_key=True)
	company = db.Column(db.String, nullable=False)
	address_1 = db.Column(db.String, nullable=False)
	address_2 = db.Column(db.String, nullable=False)
	city = db.Column(db.String, nullable=False)
	state = db.Column(db.String, nullable=False)
	zipcode = db.Column(db.String, nullable=False)
	country = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	phone = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)

	# Initialization
	def __init__(
			self,
			company,
			address_1,
			address_2,
			city,
			state,
			zipcode,
			country,
			email,
			phone,
			password):
				
		self.company = company
		self.address_1 = address_1
		self.address_2 = address_2
		self.city = city
		self.state = state
		self.zipcode = zipcode
		self.country = country
		self.email = email
		self.phone = phone
		self.password = generate_password_hash(password) 

	def is_authenticated(self):
		return True

	def is_active(self):
        	return True

	def is_anonymous(self):
        	return False

	def get_id(self):
		return unicode(self.id)

	# Handles the format when printing out a Vendor Object
	def __repr__(self):
		return '<company {}'.format(self.company)
