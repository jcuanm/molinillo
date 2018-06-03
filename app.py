from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

# Create application object
app = Flask(__name__)


app.secret_key = "my precious"       # Initializing secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///molinillo_data.db'

db = SQLAlchemy(app)
from models import *

# Custom login-required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login'))
	return wrap

@app.route('/')
def home():
	vendors = []
	if 'logged_in' in session:
		vendors = db.session.query(Vendors).all()
	return render_template('home.html', vendors=vendors)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid username or password. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('home'))

@app.route('/vendor_portal')
@login_required
def vendor_portal():
	return render_template('vendor_portal.html')

@app.route('/register')
def register():
	return render_template('register.html')


if __name__ == '__main__':
	app.run(debug=True)
