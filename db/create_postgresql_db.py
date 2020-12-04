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
cursor.execute("DROP DATABASE IF EXISTS item_db;")
cursor.execute("DROP DATABASE IF EXISTS auction_db;")
cursor.execute("DROP DATABASE IF EXISTS shopping_cart_db;")
cursor.execute("DROP DATABASE IF EXISTS notification_db;")
cursor.execute("DROP DATABASE IF EXISTS search_db;")

cursor.execute("CREATE DATABASE item_db;")
cursor.execute("CREATE DATABASE auction_db;")
cursor.execute("CREATE DATABASE shopping_cart_db;")
cursor.execute("CREATE DATABASE notification_db;")
cursor.execute("CREATE DATABASE search_db;")

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
    starting_price FLOAT NOT NULL, current_auction_price FLOAT, current_auction_buyer_id INTEGER, \
    condition INTEGER NOT NULL, image_url TEXT, shipping_cost FLOAT NOT NULL);")

cursor.execute(
    "CREATE TABLE auction_order (auction_id INTEGER NOT NULL, auction_user_id INTEGER NOT NULL, \
    item_id INTEGER NOT NULL REFERENCES item(item_id), auction_price INTEGER NOT NULL, \
    auction_time INTEGER NOT NULL, status VARCHAR(10) NOT NULL)")

category_list = [
    ("Fashion", ), ("Electronics", ), ("Motors", ), ("Collectibles", ), ("Home", ), 
    ("Sporting Goods", ), ("Toys", ), ("Business", ), ("Music", ), ("Industrial", )
]
for category in category_list:
    cursor.execute("""INSERT INTO category (category_name) VALUES (%s)""", category)

initial_image_url_1 = "https://cdn-fsly.yottaa.net/59aef05c32f01c6b98e8f0d9/www.govmint.com/v~4b.46/media/catalog/product/cache/6233b85eec3a03e6a90cf4dddd884882/1/8/184428_1.jpg?yocs=m_"
initial_image_url_2 = "https://a.1stdibscdn.com/chinese-mottled-bai-bi-disc-for-sale/1121189/f_212113721604129952175/21211372_master.jpg?disable=upscale&auto=webp&quality=60&width=960"
initial_image_url_3 = "https://a.1stdibscdn.com/mid-century-modern-baby-blue-velvet-club-armchair-1960s-for-sale/1121189/f_153838721562685325548/15383872_master.jpg?disable=upscale&auto=webp&quality=60&width=960"
initial_image_url_4 = "https://cdn-fsly.yottaa.net/59aef05c32f01c6b98e8f0d9/www.govmint.com/v~4b.46/media/catalog/product/cache/23c5af62df63748bdd45642a472f2812/1/9/1917-1-dollar-washington-legal-tender-currency-note-vf_184418_3.jpg?yocs=m_"
item_list = [
    ("1901 $10 Bison Legal Tender Note", 1, "NULL", 5, "One 1901 $10 Bison Legal Tender Note.", "ready", 
    datetime(2020, 12, 28, 10, 0, 0).timestamp(), datetime(2020, 12, 30, 10, 0, 0).timestamp(), 500, "NULL", "NULL", 7, initial_image_url_1, 0.0), 
    ("TWO JADE BI DISCS", 1, 2, 2, "The Irving Collection, New York, by 1987.", "completed", 
    datetime(2020, 11, 21, 10, 0, 0).timestamp(), datetime(2020, 11, 23, 10, 0, 0).timestamp(), 2000, 3500, 2, 2, initial_image_url_2, 10.0), 
    ("MID-CENTURY STYLE HIDE UPHOLSTERED ARMCHAIRS", 3, "NULL", 4, "a pair, each raised on splayed tapered legs to the fore 75 cm. high; 63 cm. wide; 65 cm. deep", "on-going", 
    datetime(2020, 11, 24, 10, 0, 0).timestamp(), datetime(2020, 12, 12, 10, 0, 0).timestamp(), 900, 1200, 2, 3, initial_image_url_3, 5.99), 
    ("1901 $10 Bison Legal Tender Note", 1, "NULL", 5, "One 1901 $10 Bison Legal Tender Note.", "ready", 
    datetime(2020, 11, 23, 10, 0, 0).timestamp(), datetime(2020, 11, 30, 10, 0, 0).timestamp(), 500, "NULL", "NULL", 7, initial_image_url_4, 0.0)
]
for item in item_list:
    query = """INSERT INTO item (item_name, seller_id, buyer_id, category_id, \
        description, status, auction_start_time, auction_end_time, starting_price, \
        current_auction_price, current_auction_buyer_id, condition, image_url, shipping_cost) \
        VALUES ('%s', %s, %s, %s, '%s', '%s', %d, %d, %s, %s, %s, %d, '%s', %f);""" % item
    cursor.execute(query)

auction_order_list = [
    (1, 4, 2, 3500, datetime(2020, 11, 29, 10, 0, 0).timestamp(), "valid"), 
    (2, 4, 3, 1000, datetime(2020, 11, 25, 1, 0, 0).timestamp(), "invalid"), 
    (3, 1, 3, 1100, datetime(2020, 11, 26, 1, 0, 0).timestamp(), "invalid"), 
    (4, 2, 3, 1200, datetime(2020, 11, 27, 1, 0, 0).timestamp(), "valid")
]
for order in auction_order_list:
    query = """INSERT INTO auction_order (auction_id, auction_user_id, item_id, auction_price, auction_time, status) \
        VALUES (%d, %d, %d, %f, %s, '%s')""" % order
    cursor.execute(query)


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


# # db for Search microservice





# # create tables
# item_db_cursor.execute("DROP TABLE IF EXISTS auction_log_table")
# item_db_cursor.execute("DROP TABLE IF EXISTS item_description_table")
# item_db_cursor.execute("DROP TABLE IF EXISTS item_table")


# # insert records
# item_db_cursor.execute("INSERT INTO item_table VALUES(111,'laptop', 123, NULL,'electronics', 'ready', 123, 456, 20, 123)")




