from datetime import datetime
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
    {"_id": 1, "username": "amy@mail.com", "first_name" : "Amy", "last_name": "Jhonson", "password" : "AMY", "status" : "valid", "date_joined": datetime(2020, 10, 1).strftime('%Y-%m-%d')}, 
    {"_id": 2, "username": "hannah@mail.com", "first_name" : "Hannah", "last_name": "Trump", "password" : "HANNAH", "status" : "invalid", "date_joined": datetime(2020, 10, 2).strftime('%Y-%m-%d')}, 
    {"_id": 3, "username": "michael@mail.com", "first_name" : "Michael", "last_name": "Rice", "password" : "MICHAEL", "status" : "valid", "date_joined": datetime(2020, 10, 3).strftime('%Y-%m-%d')}, 
    {"_id": 4, "username": "sandy@mail.com", "first_name" : "Sandy", "last_name": "Jhonson", "password" : "SANDY", "date_joined": datetime(2020, 10, 4).strftime('%Y-%m-%d')}, 
    {"_id": 5, "username": "betty@mail.com", "first_name" : "Betty", "last_name": "Wilson", "password" : "BETTY", "status" : "valid", "date_joined": datetime(2020, 10, 5).strftime('%Y-%m-%d')}, 
]

user_col.insert_many(user_list)
