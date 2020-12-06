from config import *

#---------- CONFIG ----------#
cursor = getDatabaseCusor(AUCTION)


#---------- DATA MODEL ----------#
AUCTION_ID = "auction_id"
AUCTION_USER_ID = "auction_user_id"
ITEM_ID = "item_id"
AUCTION_PRICE = "auction_price"
AUCTION_TIME = "auction_time"
STATUS = "status"

STATUS_VALID = "valid"
STATUS_INVALID = "invalid"

MESSAGE = "msg"
AUCTION_LIST = "auction_list"

item_client = RPCClient(AUCTION + "_" + ITEM)


class Auction(object):
    name = AUCTION

    # item_rpc = RpcProxy(ITEM)

    #@rpc
    def bid_item(self, auction_user_id, item_id, auction_price):
        # self.item_rpc.update_all_auctions_status()
        call_str = "item.update_all_auctions_status()"
        item_client.call(call_str)

        returned_data = {AUCTION_ID: None, MESSAGE: None}
        auction_time = datetime.now().timestamp()

        params = (auction_user_id, item_id, auction_price, auction_time, STATUS_INVALID)
        query = """INSERT INTO auction (auction_user_id, item_id, \
            auction_price, auction_time, status) \
            VALUES (%d, %d, %f, %d, '%s') RETURNING auction_user_id;""" % params
        try:
            cursor.execute(query)
            auction_id = cursor.fetchone()[0]
            returned_data[AUCTION_ID] = auction_id
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = auction_bid_item_failed
            return False, returned_data
        # result, msg = self.item_rpc.update_item_with_bid(auction_id, auction_user_id, item_id, auction_price, auction_time)
        call_str = "item.update_item_with_bid(%d, %d, %d, %f, %d)" % (auction_id, auction_user_id, item_id, auction_price, auction_time)
        result, msg = eval(item_client.call(call_str))

        print((result, msg))
        if result:
            returned_data[MESSAGE] = auction_bid_item_suceeded
            params = (STATUS_VALID, auction_id)
            query = """UPDATE auction SET status = '%s' WHERE auction_id = %d""" % params
            cursor.execute(query)
            return True, returned_data
        else:
            returned_data[MESSAGE] = auction_bid_item_failed
            return False, returned_data
        

    #@rpc
    def get_auction_history(self, item_id):
        # self.item_rpc.update_all_auctions_status()
        call_str = "item.update_all_auctions_status()"
        item_client.call(call_str)

        returned_data = {MESSAGE: None, AUCTION_LIST: None}
        query = "SELECT * FROM auction WHERE item_id = %s " %(item_id)

        if try_execute_sql(cursor, query, __name__):
            returned_data[MESSAGE] = auction_get_auction_history_suceeded
            data = cursor.fetchall()
            auction_list = []
            for auction_histroy in data:
                auction_list.append({
                    AUCTION_ID: auction_histroy[0],
                    AUCTION_USER_ID: auction_histroy[1],
                    ITEM_ID: auction_histroy[2],
                    AUCTION_PRICE: auction_histroy[3],
                    AUCTION_TIME: auction_histroy[4],
                    STATUS: auction_histroy[5]})

            returned_data[AUCTION_LIST] = auction_list

            return True, returned_data
        else:
            returned_data[MESSAGE] = auction_get_auction_history_failed
            return False, returned_data
        res = cursor.fetchall() 
        return True, res


def on_request(ch, method, props, body):
    print(body)
    # try:
    response = eval(body)
    # except:
    # response = False, "Exception in rpc on_request method."
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


auction = Auction()

print(" [x] Awaiting RPC requests")

channel = getRpcChannel([AUCTION])
channel.start_consuming()


