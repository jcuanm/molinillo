from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
	email = TextField("Email", validators=[DataRequired()]) 
	password = PasswordField("Password", validators=[DataRequired()]) 

# Defaults to the fields needed for a customer, and implements the Customer registration form
class CustomerRegisterForm(FlaskForm):
	username = TextField(
		'Username',
		validators=[DataRequired(), Length(min=3, max=35)]
	)

	phone = TextField(
		'Phone Number',
		validators=[Length(min=0, max=15)]
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

# Form for the account tab in the vendor portal
class AccountForm(FlaskForm):
	username = TextField(
		'Username',
		validators=[DataRequired(), Length(min=1,max=30)]
	)

	phone = TextField(
		'Phone Number',
		validators=[Length(min=0,max=15)]
	)

	street1 = TextField(
		'Street Address 1',
		validators=[Length(min=0,max=35)]
	)

	street2 = TextField(
		'Street Address 2',
		validators=[Length(min=0,max=35)]
	)

	zipcode = TextField(
		'ZIP',
		validators=[Length(min=0,max=12)]
	)

	city = TextField(
		'City',
		validators=[Length(min=0,max=30)]
	)

# Pop-up form for changing email in account tab 
class ChangeEmailForm(FlaskForm):
	email = TextField(
		'Email',
		validators=[DataRequired(), Email(message="Not a valid email.")]
	)

	change_email_password = PasswordField(
		'Password', 
		validators=[DataRequired()]
	) 

# Pop-up form for changing password in account tab 
class ChangePasswordForm(FlaskForm):
	current_password = PasswordField(
		"Current Password", 
		validators=[DataRequired()]
	) 

	new_password = PasswordField(
		'Password',
		validators=[DataRequired(), Length(min=6, max=25),EqualTo('confirm', message='Passwords must match')]
	)

	confirm = PasswordField(
		'Confirm Password'
	)

# Pop-up form for deleting a user in account tab 
class DeleteUserForm(FlaskForm):
	delete_password = PasswordField(
		'Password', 
		validators=[DataRequired()]
	) 

# Pop-up form for updatign a user's subscription in billing tab 
class UpdateSubscriptionForm(FlaskForm):
	update_subscription_password = PasswordField(
		'Password',
		validators=[DataRequired(), Length(min=1,max=30)]
	)
