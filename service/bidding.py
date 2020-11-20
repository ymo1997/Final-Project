from nameko.rpc import rpc, RpcProxy
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Item DB: item table / bidding table / shopping cart table
item_db_conn = psycopg2.connect(user = "dbuser", password = "guest",host = "localhost",port = "5432", database = "postgres")
item_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
item_db_cursor = item_db_conn.cursor()


class Bidding(object):
    name = "bidding"

    @rpc
    def list_item(self, status):
        query = "SELECT * FROM item_table WHERE status = '%s'" %(status)
        item_db_cursor.execute(query)
        res = item_db_cursor.fetchall() 
        return True, res



    @rpc
    def start_auction(self, item_id):
    	query = "SELECT bidding_start_time, status FROM item_table WHERE item_id = '%s'" %(item_id)
        item_db_cursor.execute(query)
        res = item_db_cursor.fetchall()
        bidding_start_time = int(res[0])
        status = res[1]

        current_time = 200 # for testing
        if status != "bidding":
        	if current_time > bidding_start_time:
        		query = "UPDATE item_table SET status = 'bidding' WHERE item_id = '%s'" %(item_id)
        		return True, "Start for auction."
        	else:
        		return False, "Wait for auction."

        else:
        	return False, "Already in auction"