from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(Form):
	email = TextField("Email", validators=[DataRequired()]) 
	password = PasswordField("Password", validators=[DataRequired()]) 

class RegisterForm(Form):
	company_name = TextField(
		'Company Name',
		validators=[DataRequired(), Length(min=3, max=25)]
	)

	email = TextField(
		'Email',
		validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
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

	address_1 = TextField(
		'Street Address 1',
		validators=[DataRequired(), Length(min=1, max=30)]
	)

	address_2 = TextField(
		'Street Address 2',
		validators=[Length(min=0, max=30)]
	)

	city = TextField(
		'City',
		validators=[DataRequired(), Length(min=1, max=25)]
	)

	state = TextField(
		'State',
		validators=[DataRequired(), Length(min=1, max=25)]
	)

	zipcode = TextField(
		'Zipcode',
		validators=[DataRequired(), Length(min=1, max=15)]
	)

	country = TextField(
		'Country',
		validators=[DataRequired(), Length(min=1, max=25)]
	)

	phone = TextField(
		'Phone Number',
		validators=[Length(min=0, max=30)]
	)
