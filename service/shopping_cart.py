from config import *
from json import loads, dumps

#---------- DATA MODEL ----------#
USER_ID = "user_id"
ITEM_IDS = "item_ids"

MESSAGE = "msg"
ITEM_LIST = "item_list"


#---------- CONFIG ----------#
cursor = getDatabaseCusor(SHOPPING_CART)

item_client = RPCClient(SHOPPING_CART + "_" + ITEM)

class ShoppingCart(object):
    name = SHOPPING_CART

    # item_rpc = RpcProxy(ITEM)
    
    #@rpc
    def create_user_shopping_cart(self, user_id):
        # self.item_rpc.update_all_auctions_status()
        call_str = "item.update_all_auctions_status(True)"
        add_result, add_item_id, add_user_id = eval(item_client.call(call_str))
        if add_result:
            self.add_item_to_user_shopping_cart(add_item_id, add_user_id)

        params = (user_id, "[]")
        query = """INSERT INTO shopping_cart (user_id, item_ids) VALUES (%d, '%s');""" % params

        if try_execute_sql(cursor, query, __name__):
            return True, shopping_cart_create_user_shopping_cart_suceeded
        else:
            return False, shopping_cart_create_user_shopping_cart_failed


    #@rpc
    def delete_user_shopping_cart(self, user_id):
        # self.item_rpc.update_all_auctions_status()
        call_str = "item.update_all_auctions_status(True)"
        add_result, add_item_id, add_user_id = eval(item_client.call(call_str))
        if add_result:
            self.add_item_to_user_shopping_cart(add_item_id, add_user_id)

        params = (user_id)
        query = """DELETE FROM shopping_cart WHERE user_id = %d;""" % params

        if try_execute_sql(cursor, query, __name__):
            return True, shopping_cart_delete_user_shopping_cart_suceeded
        else:
            return False, shopping_cart_delete_user_shopping_cart_failed


    #@rpc
    def add_item_to_user_shopping_cart(self, item_id, user_id):
        
        params = (user_id)
        query = """SELECT item_ids FROM shopping_cart WHERE user_id = %d;""" % params
        if not try_execute_sql(cursor, query, __name__):
            return False, shopping_cart_add_item_to_user_shopping_cart_failed

        try:
            record = loads(cursor.fetchone()[0])
            record.append(item_id)
            new_list = dumps(record)
        except Exception as e:
            log_for_except(__name__, e)
            return False, shopping_cart_add_item_to_user_shopping_cart_failed

        params = (new_list, user_id)
        query = """UPDATE shopping_cart SET item_ids = '%s' WHERE user_id = %d;""" % params
        if not try_execute_sql(cursor, query, __name__):
            return False, shopping_cart_add_item_to_user_shopping_cart_failed
        return True, shopping_cart_add_item_to_user_shopping_cart_suceeded
    

    #@rpc
    def delete_item_from_user_shopping_cart(self, item_id, user_id):        
        params = (user_id)
        query = """SELECT item_ids FROM shopping_cart WHERE user_id = %d;""" % params
        if not try_execute_sql(cursor, query, __name__):
            return False, shopping_cart_delete_item_from_user_shopping_cart_failed

        try:
            record = loads(cursor.fetchone()[0])
            new_list = dumps(record.remove(item_id))
        except Exception as e:
            log_for_except(__name__, e)
            return False, shopping_cart_delete_item_from_user_shopping_cart_failed
        
        params = (new_list, user_id)
        query = """UPDATE shopping_cart SET item_ids = '%s' WHERE user_id = %d;""" % params
        if not try_execute_sql(cursor, query, __name__):
            return False, shopping_cart_delete_item_from_user_shopping_cart_failed
        
        return True, shopping_cart_delete_item_from_user_shopping_cart_suceeded


    #@rpc
    def checkout_shopping_cart(self, user_id):
        # self.item_rpc.update_all_auctions_status()
        call_str = "item.update_all_auctions_status(True)"
        add_result, add_item_id, add_user_id = eval(item_client.call(call_str))
        if add_result:
            self.add_item_to_user_shopping_cart(add_item_id, add_user_id)

        returned_data = {ITEM_LIST: [], MESSAGE: None}

        query = """SELECT item_ids FROM shopping_cart WHERE user_id = %d;""" % int(user_id)
        if not try_execute_sql(cursor, query, __name__):
            returned_data[MESSAGE] = shopping_cart_checkout_shopping_cart_failed
            return False, returned_data

        try:
            record = loads(cursor.fetchone()[0])
            for item_id in record:
                call_str = "item.get_item_info(%d)" % item_id
                result, data = eval(item_client.call(call_str))
                price = data['current_auction_price']
                returned_data[ITEM_LIST].append({
                    'item_id': int(item_id), 'price': float(price)
                    })
            returned_data[MESSAGE] = shopping_cart_checkout_shopping_cart_suceeded
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = shopping_cart_checkout_shopping_cart_failed
            return False, returned_data

        # remove items from shopping cart
        params = ('[]', int(user_id))
        query = """UPDATE shopping_cart SET item_ids = '%s' WHERE user_id = %d;""" % params
        if not try_execute_sql(cursor, query, __name__):
            returned_data[MESSAGE] = shopping_cart_checkout_shopping_cart_failed
            return False, returned_data
        return True, returned_data


    #@rpc
    def list_user_shopping_cart_items(self, user_id):
        # self.item_rpc.update_all_auctions_status()
        call_str = "item.update_all_auctions_status(True)"
        add_result, add_item_id, add_user_id = eval(item_client.call(call_str))
        if add_result:
            self.add_item_to_user_shopping_cart(add_item_id, add_user_id)
        
        returned_data = {ITEM_LIST: [], MESSAGE: None}
        params = (user_id)
        query = "SELECT item_ids FROM shopping_cart WHERE user_id = %d;" % params

        if not try_execute_sql(cursor, query, __name__):
            returned_data[MESSAGE] = shopping_cart_list_user_shopping_cart_items_failed
            return False, returned_data
        try:
            record = loads(cursor.fetchone()[0])
            returned_data[ITEM_LIST] = record
            returned_data[MESSAGE] = shopping_cart_list_user_shopping_cart_items_suceeded
        except Exception as e:
            log_for_except(__name__, e)
            return False, shopping_cart_list_user_shopping_cart_items_failed

        return True, returned_data
    


def on_request(ch, method, props, body):
    print(body)
    try:
        response = eval(body)
    except:
        response = False, "Exception in rpc on_request method."
    ch.basic_publish(
        exchange = '',
        routing_key = props.reply_to,
        body = str(response),
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        )
    )
    ch.basic_ack(delivery_tag = method.delivery_tag)

def getRpcChannel(queue_names):
    params = pika.ConnectionParameters(host=rabbit_address)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    for queue in queue_names:
        channel.queue_declare(queue = rpc_queue_name_prefix + queue)
        channel.basic_qos(prefetch_count=prefetch_count)
        channel.basic_consume(
            queue = rpc_queue_name_prefix + queue, 
            on_message_callback = on_request
        )

    return channel


shopping_cart = ShoppingCart()

print(" [x] Awaiting RPC requests")

channel = getRpcChannel([SHOPPING_CART, USER + "_" + SHOPPING_CART, ITEM + "_" + SHOPPING_CART, ITEM + "_" + SHOPPING_CART + "2"])
channel.start_consuming()

