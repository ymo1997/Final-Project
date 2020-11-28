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
CONDITION = "condition"
IMAGE_URL = "image_url"
SHIPPING_COST = "shipping_cost"

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
    def create_item(self, item_name, seller_id, category_id, description, auction_start_time, auction_end_time, starting_price, condition, image_url, shipping_cost):
        self.update_all_auctions_status()
        status = ITEM_STATUS_READY if datetime.now().timestamp() < auction_start_time else ITEM_STATUS_ON_GOING
        returned_data = {ITEM_ID: None}
        params = (item_name, seller_id, "NULL", category_id, description, status, auction_start_time, 
            auction_end_time, starting_price, "NULL", "NULL", condition, image_url, shipping_cost)

        try:
            query = """INSERT INTO item (item_name, seller_id, buyer_id, category_id, description, status, \
            auction_start_time, auction_end_time, starting_price, current_auction_price, \
            current_auction_buyer_id, condition, image_url, shipping_cost) \
            VALUES ('%s', %s, %s, %s, '%s', '%s', %d, %d, %s, %s, %s, %d, '%s', %f) RETURNING item_id;""" % params
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
    def update_item_info(self, item_id, item_name, category_id, description, auction_start_time, auction_end_time, starting_price, condition, image_url, shipping_cost):
        self.update_all_auctions_status()
        params = (item_name, category_id, description, auction_start_time,
            auction_end_time, starting_price, condition, image_url, shipping_cost, item_id)
        try:
            query = """UPDATE item SET item_name = '%s', category_id = %d, \
                description = '%s', auction_start_time = %d, auction_end_time = %d, \
                starting_price = %f, condition = %d, image_url = '%s', shipping_cost = %f WHERE item_id = %d;""" % params
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
            query = """SELECT item_id, item_name, seller_id, buyer_id, \
            item.category_id, category_name, description, status, auction_start_time, \
            auction_end_time, starting_price, current_auction_price, \
            current_auction_buyer_id, condition, image_url, shipping_cost FROM \
            (item INNER JOIN category ON item.category_id = category.category_id) \
            WHERE item_id = %d;""" % params
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
        returned_data[CATEGORY_NAME] = record[5]
        returned_data[DESCRIPTION] = record[6]
        returned_data[STATUS] = record[7]
        returned_data[AUCTION_START_TIME] = record[8]
        returned_data[AUCTION_END_TIME] = record[9]
        returned_data[STARTING_PRICE] = record[10]
        returned_data[CURRENT_AUCTION_PRICE] = record[11]
        returned_data[CURRENT_AUCTION_BUYER_ID] = record[12]
        returned_data[CONDITION] = record[13]
        returned_data[IMAGE_URL] = record[14]
        returned_data[SHIPPING_COST] = record[15]
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
    def delete_category(self, category_id):
        self.update_all_auctions_status()
        params = (category_id)
        query = """DELETE FROM category WHERE category_id = %d""" % category_id

        if try_execute_sql(cursor, query, __name__):
            return True, item_delete_category_failed
        else:
            return False, item_delete_category_suceeded


    @rpc
    def modify_category(self, category_id, category_name):
        self.update_all_auctions_status()
        params = (category_name, category_id)
        query = """UPDATE category SET category_name = '%s' \
            WHERE category_id = %d""" % params

        if try_execute_sql(cursor, query, __name__):
            return True, item_update_category_failed
        else:
            return False, item_update_category_suceeded


    @rpc
    def list_categories(self):
        self.update_all_auctions_status()
        returned_data = {"category_list": [], MESSAGE: None}
        query = """SELECT * FROM category"""

        if try_execute_sql(cursor, query, __name__):
            records = cursor.fetchall()
            for record in records:
                temp_dict = {}
                temp_dict[CATEGORY_ID] = record[0]
                temp_dict[CATEGORY_NAME] = record[1]
                returned_data["category_list"].append(temp_dict.copy())

            returned_data[MESSAGE] = item_list_categories_failed
            return True, returned_data
        else:
            returned_data[MESSAGE] = item_list_categories_suceeded
            return False, returned_data


    @rpc
    def update_item_with_bid(self, auction_id, auction_user_id, item_id, auction_price, auction_time):
        self.update_all_auctions_status()
        query = "SELECT current_auction_price, starting_price, status FROM item WHERE item_id = %s" % (item_id)
        try:
            cursor.execute(query)
            record = cursor.fetchone()
            current_price = record[0] if record[0] is not None else record[1]
            current_status = record[2]
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
            query = """SELECT item_id, item_name, seller_id, buyer_id, \
            item.category_id, category_name, description, status, auction_start_time, \
            auction_end_time, starting_price, current_auction_price, \
            current_auction_buyer_id, condition, image_url, shipping_cost FROM \
            (item INNER JOIN category ON item.category_id = category.category_id);"""
        else:
            params = (status)
            query = """SELECT item_id, item_name, seller_id, buyer_id, \
            item.category_id, category_name, description, status, auction_start_time, \
            auction_end_time, starting_price, current_auction_price, \
            current_auction_buyer_id, condition, image_url, shipping_cost FROM \
            (item INNER JOIN category ON item.category_id = category.category_id) \
            WHERE status = '%s';""" % params

        try:
            cursor.execute(query)
            records = cursor.fetchall()
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = item_list_item_failed
            return False, returned_data

        for record in records:
            temp_dict = {}
            temp_dict[ITEM_ID] = record[0]
            temp_dict[ITEM_NAME] = record[1]
            temp_dict[SELLER_ID] = record[2]
            temp_dict[BUYER_ID] = record[3]
            temp_dict[CATEGORY_ID] = record[4]
            temp_dict[CATEGORY_NAME] = record[5]
            temp_dict[DESCRIPTION] = record[6]
            temp_dict[STATUS] = record[7]
            temp_dict[AUCTION_START_TIME] = record[8]
            temp_dict[AUCTION_END_TIME] = record[9]
            temp_dict[STARTING_PRICE] = record[10]
            temp_dict[CURRENT_AUCTION_PRICE] = record[11]
            temp_dict[CURRENT_AUCTION_BUYER_ID] = record[12]
            temp_dict[CONDITION] = record[13]
            temp_dict[IMAGE_URL] = record[14]
            temp_dict[SHIPPING_COST] = record[15]
            returned_data["item_list"].append(temp_dict.copy())
        
        returned_data[MESSAGE] = item_list_item_suceeded
        return True, returned_data


    @rpc
    def stop_item_auction(self, item_id):
        self.update_all_auctions_status()
        params = (item_id)
        query = """SELECT status FROM item WHERE item_id = %d;""" % params
        if try_execute_sql(cursor, query, __name__):
            record = cursor.fetchone()
            status = record[0]
            if status == ITEM_STATUS_ON_GOING:
                params = (ITEM_STATUS_COMPLETED, datetime.now().timestamp(), item_id)
                query = """UPDATE item SET status = '%s', auction_end_time = %d \
                WHERE item_id = %d""" % params
                if try_execute_sql(cursor, query, __name__):
                    return True, item_stop_item_auction_suceeded
        else:
            return False, item_stop_item_auction_failed


    @rpc
    def list_items_by_keyword_on_item_name(self, keyword = None):
        self.update_all_auctions_status()
        returned_data = {"item_list": [], MESSAGE: None}
        if keyword is None:
            query = """SELECT item_id, item_name, seller_id, buyer_id, \
            item.category_id, category_name, description, status, auction_start_time, \
            auction_end_time, starting_price, current_auction_price, \
            current_auction_buyer_id, condition, image_url, shipping_cost FROM \
            (item INNER JOIN category ON item.category_id = category.category_id);"""
        else:
            params = (keyword)
            query = """SELECT item_id, item_name, seller_id, buyer_id, \
            item.category_id, category_name, description, status, auction_start_time, \
            auction_end_time, starting_price, current_auction_price, \
            current_auction_buyer_id, condition, image_url, shipping_cost FROM \
            (item INNER JOIN category ON item.category_id = category.category_id) \
            WHERE lower(item_name) LIKE \'%""" + keyword.lower() + """%\';"""

        try:
            cursor.execute(query)
            records = cursor.fetchall()
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = item_list_item_by_keyword_failed
            return False, returned_data

        for record in records:
            temp_dict = {}
            temp_dict[ITEM_ID] = record[0]
            temp_dict[ITEM_NAME] = record[1]
            temp_dict[SELLER_ID] = record[2]
            temp_dict[BUYER_ID] = record[3]
            temp_dict[CATEGORY_ID] = record[4]
            temp_dict[CATEGORY_NAME] = record[5]
            temp_dict[DESCRIPTION] = record[6]
            temp_dict[STATUS] = record[7]
            temp_dict[AUCTION_START_TIME] = record[8]
            temp_dict[AUCTION_END_TIME] = record[9]
            temp_dict[STARTING_PRICE] = record[10]
            temp_dict[CURRENT_AUCTION_PRICE] = record[11]
            temp_dict[CURRENT_AUCTION_BUYER_ID] = record[12]
            temp_dict[CONDITION] = record[13]
            temp_dict[IMAGE_URL] = record[14]
            temp_dict[SHIPPING_COST] = record[14]
            returned_data["item_list"].append(temp_dict.copy())
        
        returned_data[MESSAGE] = item_items_by_keyword_suceeded
        return True, returned_data


    @rpc
    def list_items_by_category(self, category_id):
        self.update_all_auctions_status()
        returned_data = {"item_list": [], MESSAGE: None}
        params = (category_id)
        query = """SELECT item_id, item_name, seller_id, buyer_id, \
        item.category_id, category_name, description, status, auction_start_time, \
        auction_end_time, starting_price, current_auction_price, \
        current_auction_buyer_id, condition, image_url, shipping_cost FROM \
        (item INNER JOIN category ON item.category_id = category.category_id) \
        WHERE item.category_id = %d;""" % params

        try:
            cursor.execute(query)
            records = cursor.fetchall()
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = item_list_item_by_category_failed
            return False, returned_data

        for record in records:
            temp_dict = {}
            temp_dict[ITEM_ID] = record[0]
            temp_dict[ITEM_NAME] = record[1]
            temp_dict[SELLER_ID] = record[2]
            temp_dict[BUYER_ID] = record[3]
            temp_dict[CATEGORY_ID] = record[4]
            temp_dict[CATEGORY_NAME] = record[5]
            temp_dict[DESCRIPTION] = record[6]
            temp_dict[STATUS] = record[7]
            temp_dict[AUCTION_START_TIME] = record[8]
            temp_dict[AUCTION_END_TIME] = record[9]
            temp_dict[STARTING_PRICE] = record[10]
            temp_dict[CURRENT_AUCTION_PRICE] = record[11]
            temp_dict[CURRENT_AUCTION_BUYER_ID] = record[12]
            temp_dict[CONDITION] = record[13]
            temp_dict[IMAGE_URL] = record[14]
            temp_dict[SHIPPING_COST] = record[15]
            returned_data["item_list"].append(temp_dict.copy())
        
        returned_data[MESSAGE] = item_items_by_category_suceeded
        return True, returned_data


    def update_all_auctions_status(self):
        now_timestamp = datetime.now().timestamp()

        query = """SELECT item_id, seller_id, auction_start_time, \
        auction_end_time, current_auction_price, current_auction_buyer_id, status \
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
            status = record[6]
                        
            if now_timestamp >= auction_start_time:
                if now_timestamp <= auction_end_time:
                    if status != ITEM_STATUS_ON_GOING:
                        self.set_item_status_on_going(item_id)
                else:
                    if status != ITEM_STATUS_COMPLETED:
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







        

