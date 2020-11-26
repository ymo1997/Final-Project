from nameko.rpc import rpc, RpcProxy
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
from responses import *

#---------- DATA MODEL ----------#
ITEM_ID = "item_id"
ITEM_NAME = "item_name"
SELLER_ID = "seller_id"
BUYER_ID = "buyer_id"
CATEGORY_ID = "category_id"
DESCRIPTION = "description"
STATUS = "status"
AUCTION_START_TIME = "auction_start_time"
AUCTION_END_TIME = "auction_end_time"
STARTING_PRICE = "starting_price"
CURRENT_AUCTION_PRICE = "current_auction_price"
CURRENT_AUCTION_BUYER_ID = "current_auction_buyer_id"

STATUS_READY = "ready"
STATUS_ON_GOING = "on-going"
STATUS_COMPLETED = "completed"

#---------- CONFIG ----------#
server_name = "item"

item_db_conn = psycopg2.connect(
    user = "dbuser", password = "guest", host = "localhost", port = "5432", database = "item_db"
)
item_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = item_db_conn.cursor()

class item(object):
    name = server_name

    @rpc
    def create_item(self, item_name, seller_id, category_name, description, auction_start_time, auction_end_time, starting_price):
        try: 
            cursor.execute("SELECT category_id from category where category_name = %s", (category_name, ))
        except:
            return False, item_create_item_failed

        category_id = cursor.fetchone()[0]
        status = STATUS_READY if datetime.now().timestamp() < auction_start_time else STATUS_ON_GOING
        params = (item_name, seller_id, "NULL", category_id, description, status, auction_start_time, 
            auction_end_time, starting_price, "NULL", "NULL")
        query = """INSERT INTO item (item_name, seller_id, buyer_id, category_id, description, status, \
        auction_start_time, auction_end_time, starting_price, current_auction_price, current_auction_buyer_id) \
        VALUES ('%s', %s, %s, %s, '%s', '%s', %d, %d, %s, %s, %s);""" % params

        try:
            cursor.execute(query)
        except:
            return False, item_create_item_failed

        return True, item_create_item_suceeded

