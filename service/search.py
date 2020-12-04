from config import *

item_client = RPCClient(SEARCH + "_" + ITEM)


class Search(object):
    name = SEARCH

    # item_rpc = RpcProxy(ITEM)

    # @rpc
    def search_item_by_keyword(self, keyword):
        # return self.item_rpc.list_items_by_keyword_on_item_name(keyword)
        call_str = "item.list_items_by_keyword_on_item_name('%s')" % keyword
        return eval(item_client.call(call_str))


    # @rpc
    def search_item_by_category(self, category_id):
        # return self.item_rpc.list_items_by_category(category_id)
        call_str = "item.list_items_by_category(%d)" % category_id
        return eval(item_client.call(call_str))


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


search = Search()
print(" [x] Awaiting RPC requests")

channel = getRpcChannel([SEARCH, ITEM + "_" + SEARCH])
channel.start_consuming()

