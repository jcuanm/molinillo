#################

#### Imports ####

#################

from flask import Flask, render_template, redirect, url_for, request, session
from forms import * 
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
pub_key = os.environ['STRIPE_PUB_KEY'] 
secret_key = os.environ['STRIPE_SECRET_KEY'] 
stripe.api_key = secret_key

##########################

#### Helper Functions ####

##########################

# Update user's password in the database
def change_password(user, new_password):
    user.password = generate_password_hash(new_password)
    db.session.commit()

# Update user's email in the database
def change_email(user, new_email):
    user.email = new_email
    db.session.commit()

# Return the user based on the primary key id 
def get_user(user_id):
    return Users.query.filter_by(id=int(user_id)).first()

# Check if a given user is already registered given their email
def is_registered(email):
    email_mod = email.replace(" ", "") # remove any white space from email
    user = Users.query.filter_by(email=email_mod).first()
    return user != None

# Subscribes a customer to a monthly Stripe plan and returns the customer object
def subscribe_user(plan, token, email): 
    customer = stripe.Customer.create(
            plan=plan.stripe_id,
            email=email,
            source=token,
            description=plan.description
    )
    return customer

# Authenticates the user when trying to login
def authenticate_user(user, attempted_password):
    if user != None:
            return check_password_hash(user.password, attempted_password) 
    return False

# Checks if the user is a vendor or a customer and redirects appropriatel
def redirect_user(user):
    if user.urole == "VENDOR":
            return redirect(url_for('vendor_portal', 
                                    tab="products"))
    else:
            return redirect(url_for('home'))

# Handles the functionality for the Account tab in the Vendor Portal
def account(tab):
    general_info_form = AccountForm(request.form)
    change_email_form = ChangeEmailForm(request.form)
    change_password_form = ChangePasswordForm(request.form)
    delete_user_form = DeleteUserForm(request.form)
    user = get_user(current_user.get_id())

    if general_info_form.validate_on_submit(): 
            user.username = request.form['username']	
            user.street = request.form['street1']	
            # add street2!!!!!!!!!!!
            user.city = request.form['city']	
            user.zipcode = request.form['zipcode']	
            user.state = request.form['state']	
            user.country = request.form['country']	
            user.phone = request.form['phone']	
            db.session.commit()
    
    if change_email_form.validate_on_submit():
            if authenticate_user(user, request.form['change_email_password']):
                    change_email(user, request.form['email']) 	

    if change_password_form.validate_on_submit():
            if authenticate_user(user, request.form['current_password']):
                    change_password(user, request.form['new_password']) 	

    if delete_user_form.validate_on_submit(): 
            if authenticate_user(user, request.form['delete_password']):
                    logout_user()
                    
                    # Checking that the user exists in the Stripe database
                    try:
                        stripe_user = stripe.Customer.retrieve(user.stripe_id)
                        stripe_user.delete() # Deleting Stripe subscription
                        db.session.delete(user) # Deleting from Heroku DB
                        db.session.commit()
                    except:
                        # If a user does not exist on Stripe database, delete them from just the Heroku database
                        db.session.delete(user) # Deleting from Heroku DB
                        db.session.commit()
                    return redirect(url_for('home'))
            
    return render_template("/vendor_portal.html", 
			   general_info_form=general_info_form, 
			   change_email_form=change_email_form,
			   change_password_form=change_password_form,
			   delete_user_form=delete_user_form,
                           tab=tab,
			   user=user)
                          # user_id=current_user.get_id())

def billing(tab):
    print ("AHHHHHHHHHH","billing")
    return render_template("/vendor_portal.html", 
                           tab=tab)

def products(tab):
    print ("AHHHHHHHHHH","products")
    return render_template("/vendor_portal.html", 
                           tab=tab)

def history(tab):
    print ("AHHHHHHHHHH", "history")
    return render_template("/vendor_portal.html", 
                           tab=tab)

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
                            if authenticate_user(user, request.form['password']):
                                    login_user(user)
                                    return redirect_user(user)
                            else:
                                    error = 'Invalid Credentials. Please try again.'
    
    return render_template('login.html', 
                           form=form, 
                           error=error)

@app.route('/logout')
@login_required(role="ANY")
def logout():
    logout_user()
    return redirect(url_for('home'))

### WHAT IF tab IS NOT FOUND????? #####
@app.route('/vendor_portal/<tab>', methods=['GET', 'POST'])
@login_required(role="VENDOR")
def vendor_portal(tab):
    switch = {
            "account" : account,
            "billing" : billing,
            "products" : products,
            "history" : history
    }

    tab_func = switch[tab]
    return tab_func(tab)

@app.route('/vendor_register/<plan_stripe_id>', methods=['GET', 'POST'])
def vendor_register(plan_stripe_id):
    form = VendorRegisterForm(request.form)
    plan = Plans.query.filter_by(id=int(plan_stripe_id)).first()

    if form.validate_on_submit():
            token = request.form['stripeToken']
            email = request.form['stripeEmail']

            if is_registered(email):
                    error = "This email is already registered."
                    return render_template('vendor_register.html', 
                                           form=form, 
                                           pub_key=pub_key)

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

                    customer = subscribe_user(plan, token, email)
                    vendor.stripe_id = customer.id # setting the stripe_id here so that a Stripe customer is not created before a key error is made
                    db.session.add(vendor)
                    db.session.commit()
                    login_user(vendor)
                    return redirect(url_for('vendor_portal', 
                                             tab="products"))

            except KeyError: 	
                    return render_template('vendor_register.html', 
                                            form=form, 
                                            pub_key=pub_key, 
                                            amount=plan.amount)
    return render_template('vendor_register.html', 
                            form=form, 
                            pub_key=pub_key, 
                            amount=plan.amount)

@app.route('/register_options')
def register_options():
    return render_template('register_options.html')


if __name__ == '__main__':
    app.run()
