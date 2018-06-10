import os

# Default config
class BaseConfig(object):
	DEBUG = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = '\x80\xc2!\x05(`\xde\xaf\xeb\xa1`\x18D;0\xb2vud-\xf6i\x93Y'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False
