#---------- MongoDB ----------#
from datetime import datetime
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")


db_names = client.list_database_names()

def checkDB(db_name):
	if db_name in db_names:
		client.drop_database(db_name)


checkDB("admin_db")
# db for Admin microservice
admin_db = client["admin_db"]
admin_col = admin_db["admin"]
admin_list = [
    {"_id": 10001, "admin": "Yueyang@mail.com", "password" : "Zhang", "first_name": "Yueyang", "last_name": "Zhang", "date_joined": datetime(2020, 9, 1).strftime('%Y-%m-%d')}, 
    {"_id": 10002, "admin": "Anqi@mail.com", "password" : "Ni", "first_name": "Anqi", "last_name": "Ni", "date_joined": datetime(2020, 9, 1).strftime('%Y-%m-%d')}, 
    {"_id": 10003, "admin": "Huimin@mail.com", "password" : "Huang", "first_name": "Huimin", "last_name": "Huang", "date_joined": datetime(2020, 9, 2).strftime('%Y-%m-%d')}, 
    {"_id": 10004, "admin": "Yinghua@mail.com", "password" : "Mo", "first_name": "Yinghua", "last_name": "Mo", "date_joined": datetime(2020, 10, 2).strftime('%Y-%m-%d')}, 
]

admin_col.insert_many(admin_list)