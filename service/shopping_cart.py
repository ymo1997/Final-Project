from nameko.rpc import rpc, RpcProxy
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
from responses import *
from json import loads, dumps

#---------- DATA MODEL ----------#
USER_ID = "user_id"
ITEM_IDS = "item_ids"

MESSAGE = "msg"


#---------- CONFIG ----------#
server_name = "shopping_cart"

item_db_conn = psycopg2.connect(
    user = "dbuser", password = "guest", host = "localhost", port = "5432", database = "shopping_cart_db"
)
item_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = item_db_conn.cursor()


class ShoppingCart(object):
    name = server_name


    @rpc
    def create_user_shopping_cart(self, user_id):
        params = (user_id, "[]")
        query = """INSERT INTO shopping_cart (user_id, item_ids) VALUES (%d, '%s');""" % params

        if try_execute_sql(cursor, query, __name__):
            return True, shopping_cart_create_user_shopping_cart_suceeded
        else:
            return False, shopping_cart_create_user_shopping_cart_failed


    @rpc
    def delete_user_shopping_cart(self, user_id):
        params = (user_id)
        query = """DELETE FROM shopping_cart WHERE user_id = %d;""" % params

        if try_execute_sql(cursor, query, __name__):
            return True, shopping_cart_delete_user_shopping_cart_suceeded
        else:
            return False, shopping_cart_delete_user_shopping_cart_failed


    @rpc
    def add_item_to_user_shopping_cart(self, item_id, user_id):
        params = (user_id)
        query = """SELECT item_ids FROM shopping_cart WHERE user_id = %d""" % params
        if not try_execute_sql(cursor, query, __name__):
            return False, shopping_cart_add_item_to_user_shopping_cart_failed

        try:
            record = cursor.fetchone()[0]
        except Exception as e:
            log_for_except(__name__, e)
            return False, shopping_cart_add_item_to_user_shopping_cart_failed
            
        new_list = dumps(loads(record).append(item_id))

        params = (new_list, user_id)
        query = """UPDATE shopping_cart SET item_ids = '%s' WHERE user_id = %d;""" % params
        if not try_execute_sql(cursor, query, __name__):
            return False, shopping_cart_add_item_to_user_shopping_cart_failed
        return True, shopping_cart_add_item_to_user_shopping_cart_suceeded
    

    @rpc
    def delete_item_from_user_shopping_cart(self, item_id, user_id):
        params = (user_id)
        query = """SELECT item_ids FROM shopping_cart WHERE user_id = %d""" % params
        if not try_execute_sql(cursor, query, __name__):
            return False, shopping_cart_delete_item_from_user_shopping_cart_failed

        try:
            print(query)
            record = cursor.fetchone()[0]
            print(record)
            new_list = dumps(loads(record).remove(item_id))
        except Exception as e:
            log_for_except(__name__, e)
            return False, shopping_cart_delete_item_from_user_shopping_cart_failed
        
        params = (new_list, user_id)
        query = """UPDATE shopping_cart SET item_ids = '%s' WHERE user_id = %d;""" % params
        if not try_execute_sql(cursor, query, __name__):
            return False, shopping_cart_delete_item_from_user_shopping_cart_failed
        
        return True, shopping_cart_delete_item_from_user_shopping_cart_suceeded


    


