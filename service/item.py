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

ITEM_STATUS_READY = "ready"
ITEM_STATUS_ON_GOING = "on-going"
ITEM_STATUS_COMPLETED = "completed"
ITEM_STATUS_REPORTED = "reported"

MESSAGE = "msg"

CATEGORY_NAME = "category_name"

AUCTION_ORDER_STATUS_VALID = "valid"
AUCTION_ORDER_STATUS_INVALID = "invalid"

AUCTION_ID = "auction_id"
AUCTION_USER_ID = "auction_user_id"
AUCTION_PRICE = "auction_price"
AUCTION_TIME = "auction_time"

#---------- CONFIG ----------#
server_name = "item"

item_db_conn = psycopg2.connect(
    user = "dbuser", password = "guest", host = "localhost", port = "5432", database = "item_db"
)
item_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = item_db_conn.cursor()

class item(object):
    name = server_name

    shopping_cart_rpc = RpcProxy("shopping_cart")

    @rpc
    def create_item(self, item_name, seller_id, category_id, description, auction_start_time, auction_end_time, starting_price):
        self.update_all_auctions_status()
        status = ITEM_STATUS_READY if datetime.now().timestamp() < auction_start_time else ITEM_STATUS_ON_GOING
        returned_data = {ITEM_ID: None}
        params = (item_name, seller_id, "NULL", category_id, description, status, auction_start_time, 
            auction_end_time, starting_price, "NULL", "NULL")

        try:
            query = """INSERT INTO item (item_name, seller_id, buyer_id, category_id, description, status, \
            auction_start_time, auction_end_time, starting_price, current_auction_price, current_auction_buyer_id) \
            VALUES ('%s', %s, %s, %s, '%s', '%s', %d, %d, %s, %s, %s) RETURNING item_id;""" % params
            cursor.execute(query)
            returned_data[ITEM_ID] = cursor.fetchone()[0]
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = item_create_item_failed
            return False, returned_data

        returned_data[MESSAGE] = item_create_item_suceeded

        return True, returned_data


    @rpc
    def delete_item(self, item_id):
        self.update_all_auctions_status()
        try:
            query = """SELECT FROM auction_order WHERE item_id = %d""" % item_id
            cursor.execute(query)
            db_result = cursor.fetchall()
            if len(db_result) != 0:
                return False, item_delete_item_failed
        except Exception as e:
            log_for_except(__name__, e)
            return False, item_delete_item_failed

        try:
            query = """DELETE FROM item WHERE item_id = %d""" % item_id
            cursor.execute(query)
        except Exception as e:
            log_for_except(__name__, e)
            return False, item_delete_item_failed

        return True, item_delete_item_suceeded


    @rpc 
    def update_item_info(self, item_id, item_name, category_id, description, auction_start_time, auction_end_time, starting_price):
        self.update_all_auctions_status()
        params = (item_name, category_id, description, auction_start_time,
            auction_end_time, starting_price, item_id)
        try:
            query = """UPDATE item SET item_name = '%s', category_id = %d, \
                description = '%s', auction_start_time = %d, auction_end_time = %d, \
                starting_price = %f WHERE item_id = %d;""" % params
            cursor.execute(query)
        except Exception as e:
            log_for_except(__name__, e)
            return False, item_update_item_info_failed

        return True, item_update_item_info_suceeded


    @rpc 
    def get_item_info(self, item_id):
        self.update_all_auctions_status()
        returned_data = {ITEM_ID: None, ITEM_NAME: None, SELLER_ID: None, 
                        BUYER_ID: None, CATEGORY_ID: None, DESCRIPTION: None, 
                        STATUS: None, AUCTION_START_TIME: None, 
                        AUCTION_END_TIME: None, STARTING_PRICE: None, 
                        CURRENT_AUCTION_PRICE: None, CURRENT_AUCTION_BUYER_ID: None, 
                        MESSAGE: None}
        params = (item_id)
        try:
            query = """SELECT * FROM item WHERE item_id = %d;""" % params
            cursor.execute(query)
            record = cursor.fetchone()
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = item_get_item_info_failed
            return False, returned_data

        returned_data[ITEM_ID] = record[0]
        returned_data[ITEM_NAME] = record[1]
        returned_data[SELLER_ID] = record[2]
        returned_data[BUYER_ID] = record[3]
        returned_data[CATEGORY_ID] = record[4]
        returned_data[DESCRIPTION] = record[5]
        returned_data[STATUS] = record[6]
        returned_data[AUCTION_START_TIME] = record[7]
        returned_data[AUCTION_END_TIME] = record[8]
        returned_data[STARTING_PRICE] = record[9]
        returned_data[CURRENT_AUCTION_PRICE] = record[10]
        returned_data[CURRENT_AUCTION_BUYER_ID] = record[11]
        returned_data[MESSAGE] = item_get_item_info_failed

        return True, returned_data


    @rpc 
    def report_item(self, item_id):
        self.update_all_auctions_status()
        params = (ITEM_STATUS_REPORTED, item_id)
        result = self.update_item_status(params)
        if result:
            return True, item_update_item_info_suceeded
        return False, item_update_item_info_failed


    @rpc
    def create_category(self, category_name):
        self.update_all_auctions_status()
        params = (category_name)
        returned_data = {CATEGORY_ID: None}
        try:
            query = """INSERT INTO category (category_name) VALUES ('%s') RETURNING category_id;""" % params
            cursor.execute(query)
            returned_data[CATEGORY_ID] = cursor.fetchone()[0]
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = item_create_category_failed
            return False, returned_data

        returned_data[MESSAGE] = item_create_category_suceeded
        return True, returned_data

    
    @rpc
    def update_item_with_bid(self, auction_id, auction_user_id, item_id, auction_price, auction_time):
        self.update_all_auctions_status()
        query = "SELECT current_auction_price, status FROM item WHERE item_id = %s" % (item_id)
        try:
            cursor.execute(query)
            record = cursor.fetchone()
            current_price = record[0]
            current_status = record[1]
        except Exception as e:
            log_for_except(__name__, e)
            return False, item_update_item_with_bid_failed_db

        if current_status != ITEM_STATUS_ON_GOING:
            return False, item_update_item_with_bid_failed_status

        if auction_price <= current_price:
            return False, item_update_item_with_bid_failed_price
            
        params = (auction_price, auction_user_id, item_id)
        query = "UPDATE item SET current_auction_price = %s, current_auction_buyer_id = %d\
                 WHERE item_id = '%s'" % params
        try:
            cursor.execute(query)
        except Exception as e:
            log_for_except(__name__, e)
            return False, item_update_item_with_bid_failed_db

        params = (AUCTION_ORDER_STATUS_INVALID, item_id)
        query = """UPDATE auction_order SET status = '%s'\
                WHERE item_id = %d""" % params
        try:
            cursor.execute(query)
        except Exception as e:
            log_for_except(__name__, e)
            return False, item_update_item_with_bid_failed_db

        params = (item_id, auction_user_id)
        query = "SELECT * FROM auction_order WHERE item_id = %d AND auction_user_id = %d" % params
        try:
            cursor.execute(query)
            record = cursor.fetchone()
        except Exception as e:
            log_for_except(__name__, e)
            return False, item_update_item_with_bid_failed_db

        if (record is None):
            params = (auction_id, auction_user_id, item_id, 
                auction_price, auction_time, 
                AUCTION_ORDER_STATUS_VALID)
            query = """INSERT INTO auction_order (auction_id, \
                auction_user_id, item_id, auction_price, \
                auction_time, status) \
                VALUES (%d, %d, %d, %f, %s, '%s')""" % params
        else:
            params = (auction_id, auction_price, auction_time, 
                AUCTION_ORDER_STATUS_VALID, item_id, auction_user_id)
            query = """UPDATE auction_order SET \
                    auction_id = %d, auction_price = %f, \
                    auction_time = %d, status = '%s' \
                    WHERE item_id = %d AND auction_user_id = %d""" % params

        try:
            cursor.execute(query)
        except Exception as e:
            log_for_except(__name__, e)
            return False, item_update_item_with_bid_failed_db

        return True, item_update_item_with_bid_suceeded


    @rpc
    def list_user_auctioning(self, auction_user_id):
        self.update_all_auctions_status()
        returned_data = {"auction_list": [], MESSAGE: None}
        params = (auction_user_id)
        try:
            query = """SELECT * FROM auction_order WHERE auction_user_id = %d;""" % params
            cursor.execute(query)
            records = cursor.fetchall()
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = item_list_user_auctioning_failed
            return False, returned_data

        for record in records:
            temp_dict = {}
            temp_dict[AUCTION_ID] = record[0]
            temp_dict[AUCTION_USER_ID] = record[1]
            temp_dict[ITEM_ID] = record[2]
            temp_dict[AUCTION_PRICE] = record[3]
            temp_dict[AUCTION_TIME] = record[4]
            temp_dict[STATUS] = record[5]
            returned_data["auction_list"].append(temp_dict.copy())
        
        returned_data[MESSAGE] = item_list_user_auctioning_suceeded
        return True, returned_data


    @rpc
    def list_items(self, status = None):
        self.update_all_auctions_status()
        returned_data = {"item_list": [], MESSAGE: None}
        if status is None:
            query = """SELECT * FROM item;"""
        else:
            params = (status)
            query = """SELECT * FROM item WHERE status = '%s';""" % params

        try:
            cursor.execute(query)
            records = cursor.fetchall()
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = item_list_item_failed
            return False, returned_data

        for record in records:
            temp_dict = {}
            temp_dict[AUCTION_ID] = record[0]
            temp_dict[AUCTION_USER_ID] = record[1]
            temp_dict[ITEM_ID] = record[2]
            temp_dict[AUCTION_PRICE] = record[3]
            temp_dict[AUCTION_TIME] = record[4]
            temp_dict[STATUS] = record[5]
            returned_data["item_list"].append(temp_dict.copy())
        
        returned_data[MESSAGE] = item_list_item_suceeded
        return True, returned_data


    def update_all_auctions_status(self):
        now_timestamp = datetime.now().timestamp()

        query = """SELECT item_id, seller_id, auction_start_time, \
        auction_end_time, current_auction_price, current_auction_buyer_id \
        FROM item"""

        try:
            cursor.execute(query)
            records = cursor.fetchall()
        except Exception as e:
            log_for_except(__name__, e)
            return

        for record in records:
            item_id = record[0]
            seller_id = record[1]
            auction_start_time = record[2]
            auction_end_time = record[3]
            current_auction_price = record[4]
            current_auction_buyer_id = record[5]
                        
            if now_timestamp >= auction_start_time:
                if now_timestamp <= auction_end_time:
                    self.set_item_status_on_going(item_id)
                else:
                    self.set_item_status_completed(item_id, current_auction_buyer_id)


    def set_item_status_on_going(self, item_id):
        params = (ITEM_STATUS_ON_GOING, item_id)
        self.update_item_status(params)
        

    def set_item_status_completed(self, item_id, user_id):
        params = (ITEM_STATUS_COMPLETED, item_id)
        self.update_item_status(params)

        if user_id is not None:
            self.shopping_cart_rpc.add_item_to_user_shopping_cart(item_id, user_id)

            params = (user_id, item_id)
            query = "UPDATE item SET buyer_id = %d WHERE item_id = %d" % params
            return try_execute_sql(cursor, query, __name__)


    def update_item_status(self, params):
        query = "UPDATE item SET status = '%s' WHERE item_id = %d" % params
        return try_execute_sql(cursor, query, __name__)







        

