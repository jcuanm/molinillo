from flask import Flask, render_template, redirect, url_for, request
from form import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from functools import wraps
import os

# Create application object
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
from models import *
login_manager.login_view = '/login'

@login_manager.user_loader
def load_vendor(vendor_id):
	return Vendors.query.filter(Vendors.id == int(vendor_id)).first()

# Home page routing
@app.route('/')
def home():
	vendors = []
	if current_user.is_authenticated():
		vendors = db.session.query(Vendors).all()
	return render_template('home.html', vendors=vendors)

# About page routing
@app.route('/about')
def about():
	return render_template('about.html')

# Login page routing
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			vendor = Vendors.query.filter_by(email=request.form['email']).first()
			if vendor != None and pbkdf2_sha256.verify(request.form['password'], vendor.password):
				login_user(vendor)
				return redirect(url_for('home'))
			else:
				error = 'Invalid Credentials. Please try again.'
	
	return render_template('login.html', form=form, error=error)

# Execute Logout if logged in
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
