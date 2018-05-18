import sqlite3

with sqlite3.connect("molinillo_data.db") as connection:
	cursor = connection.cursor()
	#cursor.execute("""DROP TABLE vendors""")
	cursor.execute("""CREATE TABLE vendors(
											id Integer PRIMARY KEY AUTOINCREMENT, 
											biz_name TEXT, 
											street_address_1 TEXT, 
											street_address_2 TEXT, 
											city TEXT, 
											state_province_region TEXT, 
											zip TEXT, 
											country TEXT, 
											email TEXT, 
											phone TEXT)
										""")

	cursor.execute("""INSERT INTO vendors (biz_name,street_address_1,street_address_2, city, state_province_region, zip, country, email, phone) VALUES(
												"molinillo", 
												"64 Linnaean St.", 
												"", 
												"Cambridge", 
												"MA", 
												"02138", 
												"USA", 
												"jcuanm@gmail.com", 
												"9518162589")
											""")
