import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")

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


# # docker run -it -d --rm --name postgresql -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# item_db_conn = psycopg2.connect(user = "dbuser", password = "guest",host = "localhost",port = "5432", database = "postgres")
# item_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# item_db_cursor = item_db_conn.cursor()
# cursor.execute("CREATE DATABASE item_db")



