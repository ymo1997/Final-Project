import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

def get_db_cursor(db_name):
    postgresql_conn = psycopg2.connect(user = "dbuser", password = "guest", host = "localhost", port = "5432", database = db_name)
    postgresql_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return postgresql_conn.cursor()

cursor = get_db_cursor("postgres")
cursor.execute("DROP DATABASE IF EXISTS shopping_cart_db;")
cursor.execute("CREATE DATABASE shopping_cart_db;")

# # db for Shopping_Cart microservice
cursor = get_db_cursor("shopping_cart_db")
cursor.execute("DROP TABLE IF EXISTS shopping_cart;")
cursor.execute("CREATE TABLE shopping_cart (user_id INTEGER NOT NULL, item_ids TEXT NOT NULL)")
cart_list = [
    (1, '[]'),
    (2, '[2]'),
    (3, '[]'),
    (4, '[]'),
    (5, '[]'),
]
for cart in cart_list:
    query = """INSERT INTO shopping_cart (user_id, item_ids) VALUES (%d, '%s');""" % cart
    cursor.execute(query)
