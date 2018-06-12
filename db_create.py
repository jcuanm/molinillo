from app import db
from models import Users

# Create the database and its tables
db.create_all()

#insert
db.session.add(Users(
"molinillo1", 
"64dwdb", 
"", 
"Cambridge", 
"MA", 
"02138", 
"USA", 
"jcuanm@gmail.com", 
"9518162589",
"it's a secret",
"VENDOR"))

db.session.add(Users(
"javi", 
"fakes address", 
"another fake address", 
"Ranchoi", 
"CA", 
"91739", 
"USA", 
"yo@whatup.com", 
"9518162555",
"password",
"CUSTOMER"))

#commit
db.session.commit()
