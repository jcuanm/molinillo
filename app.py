#################

#### Imports ####

#################

from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm, CustomerRegisterForm, VendorRegisterForm 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from functools import wraps
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

##########################

#### Helper Functions ####

##########################

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
			user = Users.query.filter_by(email=request.form['email']).first()
			if is_valid_user(user, request.form['password']):
				login_user(user)
				return redirect_user(user.urole)
			else:
				error = 'Invalid Credentials. Please try again.'
	else:
		if current_user.is_authenticated():
			error = "You're already logged in. Please logout to switch accounts."
	
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

@app.route('/vendor_register', methods=['GET', 'POST'])
def vendor_register():
	form = VendorRegisterForm()
	if form.validate_on_submit():
		vendor = Users(
				username=form.username.data,
				address_1=form.address_1.data,
				address_2=form.address_2.data,
				city=form.city.data,
				state=form.state.data,
				zipcode=form.zipcode.data,
				country=form.country.data,
				email=form.email.data,
				phone=form.phone.data,
				password=form.password.data,
				urole="VENDOR"
			)
		db.session.add(vendor)
		db.session.commit()
		login_user(vendor)
		return redirect(url_for('vendor_portal'))
	return render_template('vendor_register.html', form=form)

@app.route('/register_options')
def register_options():
	return render_template('register_options.html')

if __name__ == '__main__':
	app.run()
