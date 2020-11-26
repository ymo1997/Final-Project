#---------- MongoDB ----------#

import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")

db_names = client.list_database_names()

def checkDB(db_name):
	if db_name in db_names:
		client.drop_database(db_name)

checkDB("user_db")
# db for User microservice
user_db = client["user_db"]
user_col = user_db["user"]
user_list = [
    {"_id": 1, "username" : "Amy", "password" : "AMY", "status" : "valid", "sex": "female", "age": 20, "credit": 40000}, 
    {"_id": 2, "username" : "Hannah", "password" : "HANNAH", "status" : "invalid", "sex": "female", "age": 25, "credit": 45000}, 
    {"_id": 3, "username" : "Michael", "password" : "MICHAEL", "status" : "valid", "sex": "male", "age": 30, "credit": 1000}, 
    {"_id": 4, "username" : "Sandy", "password" : "SANDY", "status" : "valid", "sex": "female", "age": 32, "credit": 3000}, 
    {"_id": 5, "username" : "Betty", "password" : "BETTY", "status" : "valid", "sex": "female", "age": 50, "credit": 10000}, 
]

user_col.insert_many(user_list)

checkDB("admin_db")
# db for Admin microservice
admin_db = client["admin_db"]
admin_col = admin_db["admin"]
admin_list = [
    {"_id": 1, "admin": "Yueyang", "password" : "Zhang"}, 
    {"_id": 2, "admin": "Anqi", "password" : "Ni"}, 
    {"_id": 3, "admin": "Huimin", "password" : "Huang"}, 
    {"_id": 4, "admin": "Yinghua", "password" : "Mo"}, 
]

admin_col.insert_many(admin_list)

# db for Login microservice



#---------- Postgresql ----------#

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

def get_db_cursor(db_name):
    postgresql_conn = psycopg2.connect(user = "dbuser", password = "guest", host = "localhost", port = "5432", database = db_name)
    postgresql_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return postgresql_conn.cursor()

# create dbs

cursor = get_db_cursor("postgres")
# cursor.execute("DROP DATABASE IF EXISTS item_db;")
# cursor.execute("DROP DATABASE IF EXISTS auction_db;")
# cursor.execute("DROP DATABASE IF EXISTS shopping_cart_db;")
# cursor.execute("DROP DATABASE IF EXISTS notification_db;")
# cursor.execute("DROP DATABASE IF EXISTS search_db;")

# cursor.execute("CREATE DATABASE item_db;")
# cursor.execute("CREATE DATABASE auction_db;")
# cursor.execute("CREATE DATABASE shopping_cart_db;")
# cursor.execute("CREATE DATABASE notification_db;")
# cursor.execute("CREATE DATABASE search_db;")

# db for Item microservice
cursor = get_db_cursor("item_db")
cursor.execute("DROP TABLE IF EXISTS auction_order;")
cursor.execute("DROP TABLE IF EXISTS item;")
cursor.execute("DROP TABLE IF EXISTS category;")

cursor.execute(
    "CREATE TABLE category (category_id SERIAL PRIMARY KEY, category_name VARCHAR(32))")

cursor.execute(
    "CREATE TABLE item (\
    item_id SERIAL PRIMARY KEY, item_name VARCHAR(255) NOT NULL, seller_id INTEGER NOT NULL, \
    buyer_id INTEGER, category_id INTEGER NOT NULL REFERENCES category(category_id), description TEXT, \
    status VARCHAR(10) NOT NULL, auction_start_time INTEGER NOT NULL, auction_end_time INTEGER NOT NULL, \
    starting_price FLOAT NOT NULL, current_auction_price FLOAT, current_auction_buyer_id INTEGER);")

cursor.execute(
    "CREATE TABLE auction_order (auction_id SERIAL PRIMARY KEY, auction_user_id INTEGER NOT NULL, \
    item_id INTEGER NOT NULL REFERENCES item(item_id), auction_price INTEGER NOT NULL, \
    auction_time INTEGER NOT NULL, status VARCHAR(10) NOT NULL)")

category_list = [
    ("Art", ), ("Jewelry", ), ("Asian Antiques", ), ("Furniture", ), ("Collectibles", ), 
    ("Coins", ), ("Memorabilia", ), ("Home & Garden", ), ("Fashion", )
]
for category in category_list:
    cursor.execute("""INSERT INTO category (category_name) VALUES (%s)""", category)

item_list = [
    ("1901 $10 Bison Legal Tender Note", 1, "NULL", 5, "One 1901 $10 Bison Legal Tender Note.", "ready", 
    datetime(2020, 11, 28, 10, 0, 0).timestamp(), datetime(2020, 11, 30, 10, 0, 0).timestamp(), 500, "NULL", "NULL"), 
    ("TWO JADE BI DISCS", 1, 2, 2, "The Irving Collection, New York, by 1987.", "completed", 
    datetime(2020, 11, 21, 10, 0, 0).timestamp(), datetime(2020, 11, 23, 10, 0, 0).timestamp(), 2000, 3500, 2), 
    ("MID-CENTURY STYLE HIDE UPHOLSTERED ARMCHAIRS", 3, "NULL", 4, "a pair, each raised on splayed tapered legs to the fore 75 cm. high; 63 cm. wide; 65 cm. deep", "on-going", 
    datetime(2020, 11, 24, 10, 0, 0).timestamp(), datetime(2020, 12, 12, 10, 0, 0).timestamp(), 900, 1200, 2)
]
for item in item_list:
    query = """INSERT INTO item (item_name, seller_id, buyer_id, category_id, description, status, \
        auction_start_time, auction_end_time, starting_price, current_auction_price, current_auction_buyer_id) \
        VALUES ('%s', %s, %s, %s, '%s', '%s', %d, %d, %s, %s, %s);""" % item
    cursor.execute(query)

auction_order_list = [
    (4, 2, 3500, datetime.now().timestamp(), "valid"), 
    (4, 3, 1000, datetime.now().timestamp(), "invalid"), 
    (1, 3, 1100, datetime.now().timestamp(), "invalid"), 
    (2, 3, 1200, datetime.now().timestamp(), "valid")
]
for order in auction_order_list:
    query = """INSERT INTO auction_order (auction_user_id, item_id, auction_price, auction_time, status) \
        VALUES (%d, %d, %f, %s, '%s')""" % order
    cursor.execute(query)



# # db for Auction microservice
# item_db_conn = psycopg2.connect(user = "dbuser", password = "guest", host = "localhost", port = "5432", database = "auction_db")
# item_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# item_db_cursor = item_db_conn.cursor()
# item_db_cursor.execute("DROP DATABASE IF EXISTS auction_db;")



# # db for Shopping_Cart microservice


# item_db_cursor.execute(
#     "CREATE TABLE shopping_cart_table (cart_id INTEGER PRIMARY KEY, item_id INTEGER REFERENCES item_table(item_id), \
#     buyer_id INTEGER)")
# # db for Notification microservice

# # db for Search microservice





# # create tables
# item_db_cursor.execute("DROP TABLE IF EXISTS auction_log_table")
# item_db_cursor.execute("DROP TABLE IF EXISTS item_description_table")
# item_db_cursor.execute("DROP TABLE IF EXISTS item_table")


# # insert records
# item_db_cursor.execute("INSERT INTO item_table VALUES(111,'laptop', 123, NULL,'electronics', 'ready', 123, 456, 20, 123)")





