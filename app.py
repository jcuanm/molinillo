#################

#### imports ####

#################

from flask import Flask, render_template, redirect, url_for, request
from form import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from functools import wraps
import os

########################

#### Configurations ####

########################

app = Flask(__name__)
login_manager = LoginManager() 
login_manager.init_app(app) # Using Flask Login-Forms to login the users
app.config.from_object(os.environ['APP_SETTINGS']) # Setting environment variables
db = SQLAlchemy(app) # Using SQLAlchemy to handle SQL queries
from models import *
login_manager.login_view = '/login'

##########################

#### Helper Functions ####

##########################

# Authenticates the vendor when trying to login
def is_valid_vendor(vendor, vendor_password_hash, attempted_password):
	return vendor != None and check_password_hash(vendor_password_hash, attempted_password) 

@login_manager.user_loader
def load_vendor(vendor_id):
	return Vendors.query.filter(Vendors.id == int(vendor_id)).first()

#################

#### Routes ####

#################

### Use decorators to link the functions to a url ###

@app.route('/')
def home():
	vendors = []
	if current_user.is_authenticated():
		vendors = db.session.query(Vendors).all()
	return render_template('home.html', vendors=vendors)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			vendor = Vendors.query.filter_by(email=request.form['email']).first()
			if is_valid_vendor(vendor, vendor.password, request.form['password']):
				login_user(vendor)
				return redirect(url_for('home'))
			else:
				error = 'Invalid Credentials. Please try again.'
	
	return render_template('login.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/vendor_portal')
@login_required
def vendor_portal():
	return render_template('vendor_portal.html')

@app.route('/register')
def register():
	return render_template('register.html')


if __name__ == '__main__':
	app.run()
