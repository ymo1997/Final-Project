############## Mongo ################

import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")


dbnames = client.list_database_names()

def checkDB(dbname):
	if dbname in dbnames:
		client.drop_database(dbname)

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


############## Postgres ################

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Item DB: item table / bidding table / shopping cart table
item_db_conn = psycopg2.connect(user = "dbuser", password = "guest",host = "localhost",port = "5432", database = "postgres")
item_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
item_db_cursor = item_db_conn.cursor()

try:
    item_db_cursor.execute("CREATE DATABASE item_db")
except:
    pass

# create tables
item_db_cursor.execute("DROP TABLE IF EXISTS bidding_log_table")
item_db_cursor.execute("DROP TABLE IF EXISTS item_description_table")
item_db_cursor.execute("DROP TABLE IF EXISTS item_table")
item_db_cursor.execute(
                "CREATE TABLE item_table (\
                item_id INTEGER PRIMARY KEY, item_name VARCHAR(15) NOT NULL, seller_id INTEGER NOT NULL, buyer_id INTEGER, \
                catagory VARCHAR(15), status VARCHAR(10) NOT NULL, bidding_start_time INTEGER NOT NULL, \
                bidding_end_time INTEGER NOT NULL, current_bidding_price INTEGER, current_bidding_buyer_id INTEGER)")
item_db_cursor.execute(
                "CREATE TABLE bidding_log_table (bidding_id INTEGER PRIMARY KEY, item_id INTEGER REFERENCES item_table(item_id), \
                bidding_buyer_id VARCHAR(15) NOT NULL, bidding_price INTEGER NOT NULL, time_stamp INTEGER NOT NULL)")
item_db_cursor.execute(
                "CREATE TABLE item_description_table (item_id INTEGER PRIMARY KEY REFERENCES item_table(item_id), \
                description TEXT)")

# insert records
item_db_cursor.execute("INSERT INTO item_table VALUES(111,'laptop', 123, NULL,'electronics', 'ready', 123, 456, 20, 123)")




