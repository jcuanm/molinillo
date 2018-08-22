from app import db
from models import Users, Plans

# Create the database and its tables
db.create_all()
'''
#insert
db.session.add(Users(
"molinillo1", 
"64dwdb", 
"Cambridge", 
"MA", 
"02138", 
"USA", 
"jcuanm@gmail.com", 
"9518162589",
"it's a secret",
"VENDOR",
"cus_4fdAW5ftNQow1a"))

db.session.add(Users(
"javi", 
"fakes address", 
"Ranchoi", 
"CA", 
"91739", 
"USA", 
"yo@whatup.com", 
"9518162555",
"password",
"CUSTOMER",
"cus_4fdAW5ftNQow1a"))
'''
db.session.add(Plans(
"plan_DSJ2J4GWgA6gV7", 
1500,
"Standard monthly vendor subscription"))

db.session.add(Plans(
"plan_DSJ5PYWe9JZnuh", 
3200,
"Gold monthly vendor subscription"))

#commit
db.session.commit()
