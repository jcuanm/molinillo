import os

# Default config
class BaseConfig(object):
	DEBUG = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ['SECRET_KEY']	
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	STRIPE_PUB_KEY = os.environ['STRIPE_PUB_KEY']
	STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']

class DevelopmentConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False
