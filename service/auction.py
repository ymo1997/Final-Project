from nameko.rpc import rpc, RpcProxy
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

# Item DB: item table / auction table / shopping cart table
item_db_conn = psycopg2.connect(user = "dbuser", password = "guest",host = "localhost",port = "5432", database = "postgres")
item_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
item_db_cursor = item_db_conn.cursor()


class Auction(object):
    name = "auction"

    @rpc
    def list_item(self, status):
        query = "SELECT * FROM item_table WHERE status = '%s'" %(status)
        item_db_cursor.execute(query)
        res = item_db_cursor.fetchall() 
        return True, res

    @rpc
    def update_auction_status(self, item_id):
        # we have three status 'ready', 'auction', 'completed'
        query = "SELECT auction_start_time, auction_end_time, status FROM item_table WHERE item_id = %s" %(item_id)
        item_db_cursor.execute(query)
        res = item_db_cursor.fetchone()

        auction_start_time = int(res[0])
        auction_end_time = int(res[1])
        status = str(res[2])

        current_time = time.time()
        new_status = None

        if current_time < auction_start_time:
            if status == "ready":
                return False, "ready"
            else:
                new_status = "ready"
        elif auction_start_time <= current_time <= auction_end_time:
            if status == "auction":
                return False, "auction"
            else:
                new_status = "auction"
        else:
            if status == "completed":
                return False, "completed"
            else:
                new_status = "completed"

        if new_status:
            query = "UPDATE item_table SET status = '%s' WHERE item_id = '%s'" %(new_status, item_id)
            item_db_cursor.execute(query)
            return True, new_status

    @rpc
    def set_auction_window(self, item_id, start_time, end_time):
        if end_time <= start_time:
            return False, "Failed: End time must be larger than start time."
        
        query = "UPDATE item_table SET auction_start_time = '%s', auction_end_time = '%s'\
                 WHERE item_id = '%s'" %(start_time, end_time, item_id)
        item_db_cursor.execute(query)
        return True, "Succeeded"

    @rpc
    def increment_bidding_price(self, item_id, user_id, new_price):
        query = "SELECT current_auction_price FROM item_table WHERE item_id = %s" %(item_id)
        item_db_cursor.execute(query)
        old_price = int(item_db_cursor.fetchone()[0])
        if new_price < old_price:
            return False, "Failed: Need to bid a higher price."
        query = "UPDATE item_table SET current_auction_price = %s, current_auction_buyer_id = %s\
                 WHERE item_id = '%s'" %(new_price, user_id, item_id)
        item_db_cursor.execute(query)
        return True, "Succeeded"




    ####### for testing/admin ######'
    @rpc
    def change_bidding_price(self, item_id, user_id, new_price):
        query = "UPDATE item_table SET current_auction_price = %s, current_auction_buyer_id = %s\
                 WHERE item_id = '%s'" %(new_price, user_id, item_id)
        item_db_cursor.execute(query)
        return True, "Succeeded"



    @rpc
    def change_auction_status(self, item_id, new_status):
        # Used for testing/admin, change auction status without checking anything
        query = "UPDATE item_table SET status = '%s' WHERE item_id = '%s'" %(new_status, item_id)
        item_db_cursor.execute(query)
        return True, new_status






