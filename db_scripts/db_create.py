from app import db
from models import Users, Plans, States

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

db.session.add(Plans(
"plan_D656saUwDokACG", 
3000,
"Molinillo monthly vendor subscription: tier 1"))

db.session.add(Plans(
"plan_D6Fm4sUCcQMI7Y", 
4000,
"Molinillo monthly vendor subscription: tier 2"))

db.session.add(Plans(
"plan_D6FmHzYYgTpPfV", 
6000,
"Molinillo monthly vendor subscription: tier 3"))
'''


#commit
db.session.commit()
