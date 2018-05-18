from flask import Flask, render_template, redirect, url_for, request, session
from functools import wraps
import sqlite3

# Create application object
app = Flask(__name__)

# Initializing secret key
app.secret_key = "my precious"
app.database = "molinillo_data.db"

# Custom login required decorator
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
	return render_template('home.html')

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

# Makes the initial connection to the molinillo_data.db
def connect_db():
	return sqlite3.connect(app.database)

if __name__ == '__main__':
	app.run(debug=True)
