#################

#### Imports ####

#################

from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm, CustomerRegisterForm, VendorRegisterForm 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from functools import wraps
import stripe
import os

############################

#### App Configurations ####

############################

app = Flask(__name__)
login_manager = LoginManager() 
login_manager.init_app(app) # Using Flask-Login Forms to login the users
app.config.from_object(os.environ['APP_SETTINGS']) # Setting environment variables
db = SQLAlchemy(app) # Using SQLAlchemy to handle SQL queries
from models import *
login_manager.login_view = '/login'
pub_key = "pk_test_AfpQRYMDWhhU0socYbDIVIUF" # MAKE ENVIORNMENT VARIABLE
secret_key = "sk_test_gvVVUcsKVEhsHXL5B7EEMa8I" # MAKE ENVIORNMENT VARIABLE
stripe.api_key = secret_key

##########################

#### Helper Functions ####

##########################

# Subscribes a customer to a monthly Stripe plan and returns the customer object
def subscribe_user(plan_stripe_id, token, email): 
	plan = Plans.query.filter_by(id=int(plan_stripe_id)).first()
	customer = stripe.Customer.create(
		plan=plan.stripe_id,
		email=email,
		source=token,
		description=plan.description
	)
	return customer

# Authenticates the user when trying to login
def is_valid_user(user, attempted_password):
	if user != None:
		return check_password_hash(user.password, attempted_password) 
	return False

# Checks if the user is a vendor or a customer and redirects appropriatel
def redirect_user(urole):
	if urole == "VENDOR":
		return redirect(url_for('vendor_portal'))
	else:
		return redirect(url_for('home'))

# This decorator restricts access to vendors and users to certain url (role can take 3 values: CUSTOMER, VENDOR, or ANY)
def login_required(role="ANY"):
	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):
			if not current_user.is_authenticated():
				return login_manager.unauthorized()
			if ((current_user.urole != role) and (role != "ANY")):
				return login_manager.unauthorized()      
			return fn(*args, **kwargs)
		return decorated_view
	return wrapper

# Loads the user upon successful login
@login_manager.user_loader
def load_user(user_id):
	return Users.query.filter(Users.id == int(user_id)).first()

#################

#### Routes ####

#################

### Use decorators to link the functions to a url ###

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			if current_user.is_authenticated():
				error = "You're already logged in. Please logout to switch accounts."
			else:
				user = Users.query.filter_by(email=request.form['email']).first()
				if is_valid_user(user, request.form['password']):
					login_user(user)
					return redirect_user(user.urole)
				else:
					error = 'Invalid Credentials. Please try again.'
	
	return render_template('login.html', form=form, error=error)

@app.route('/logout')
@login_required(role="ANY")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/vendor_portal')
@login_required(role="VENDOR")
def vendor_portal():
	users = []
	if current_user.is_authenticated():
		users = db.session.query(Users).all()
	return render_template('vendor_portal.html', users=users)

@app.route('/vendor_register/<plan_stripe_id>', methods=['GET', 'POST'])
def vendor_register(plan_stripe_id):
	form = VendorRegisterForm()

	if form.validate_on_submit():

		token = request.form['stripeToken']
		email = request.form['stripeEmail']

		try:

			vendor = Users(
					username=form.username.data,
					phone=form.phone.data,
					password=form.password.data,
					street=request.form['stripeBillingAddressLine1'],
					city=request.form['stripeBillingAddressCity'],
					state=request.form['stripeBillingAddressState'],
					zipcode=request.form['stripeBillingAddressZip'],
					country=request.form['stripeBillingAddressCountry'],
					email=email,
					urole="VENDOR",
					stripe_id=None,
					plan=plan_stripe_id
				)

			customer = subscribe_user(plan_stripe_id, token, email)
			vendor.stripe_id = customer.id # setting the stripe_id here so that a Stripe customer is not created before a key error is made
			db.session.add(vendor)
			db.session.commit()
			login_user(vendor)
			return redirect(url_for('vendor_portal'))

		except KeyError: 	
			return render_template('vendor_register.html', form=form, pub_key=pub_key)
	return render_template('vendor_register.html', form=form, pub_key=pub_key)

@app.route('/register_options')
def register_options():
	return render_template('register_options.html')

if __name__ == '__main__':
	app.run()
