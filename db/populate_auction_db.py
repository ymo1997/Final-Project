import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

def get_db_cursor(db_name):
    postgresql_conn = psycopg2.connect(user = "dbuser", password = "guest", host = "localhost", port = "5432", database = db_name)
    postgresql_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return postgresql_conn.cursor()

cursor = get_db_cursor("postgres")
cursor.execute("DROP DATABASE IF EXISTS auction_db;")
cursor.execute("CREATE DATABASE auction_db;")

# db for Auction microservice
cursor = get_db_cursor("auction_db")
cursor.execute("DROP TABLE IF EXISTS auction;")
cursor.execute(
    "CREATE TABLE auction (auction_id SERIAL PRIMARY KEY, auction_user_id INTEGER NOT NULL, \
    item_id INTEGER NOT NULL, auction_price INTEGER NOT NULL, auction_time INTEGER NOT NULL, \
    status VARCHAR(15) NOT NULL)")
auction_list = [
    (4, 2, 3500, datetime(2020, 11, 29, 10, 0, 0).timestamp(), 'valid'), 
    (4, 3, 1000, datetime(2020, 11, 25, 1, 0, 0).timestamp(), 'valid'), 
    (1, 3, 1100, datetime(2020, 11, 26, 1, 0, 0).timestamp(), 'valid'), 
    (2, 3, 1200, datetime(2020, 11, 27, 1, 0, 0).timestamp(), 'valid')
]
for auction in auction_list:
    query = """INSERT INTO auction (auction_user_id, item_id, auction_price, auction_time, status) \
        VALUES (%d, %d, %f, %d, '%s');""" % auction
    cursor.execute(query)


