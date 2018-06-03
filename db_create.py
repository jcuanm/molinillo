from app import db
from models import Vendors

# Create the database and its tables
db.create_all()

#insert
db.session.add(Vendors(
"molinillo1", 
"64dwdb", 
"", 
"Cambridge", 
"MA", 
"02138", 
"USA", 
"jcuanm@gmail.com", 
"9518162589"))

db.session.add(Vendors(
"javi", 
"fakes address", 
"another fake address", 
"Ranchoi", 
"CA", 
"91739", 
"USA", 
"yo@whatup.com", 
"9518162555"))

#commit
db.session.commit()
