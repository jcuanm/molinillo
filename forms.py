from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
	email = TextField("Email", validators=[DataRequired()]) 
	password = PasswordField("Password", validators=[DataRequired()]) 

# Defaults to the fields needed for a customer, and implements the Customer registration form
class CustomerRegisterForm(FlaskForm):
	username = TextField(
		'Username',
		validators=[DataRequired(), Length(min=3, max=25)]
	)

	phone = TextField(
		'Phone Number',
		validators=[Length(min=0, max=30)]
	)

	password = PasswordField(
		'Password',
		validators=[DataRequired(), Length(min=6, max=25)]
	)

	confirm = PasswordField(
		'Confirm Password',
		validators=[
			DataRequired(), EqualTo('password', message='Passwords must match.')
		]
	)

# Inherits from User class and implements the Vendor registration form 
class VendorRegisterForm(CustomerRegisterForm):
	username = TextField(
		'Vendor Name',
		validators=[DataRequired(), Length(min=3, max=25)]
	)
