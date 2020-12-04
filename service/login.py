from config import *

#---------- DATA MODEL ----------#
IS_ADMIN = "is_admin"
ID = "_id"

MESSAGE = "msg"

user_client = RPCClient(LOGIN + "_" + USER)
admin_client = RPCClient(LOGIN + "_" + ADMIN)

class Login(object):
    name = LOGIN

    # user_rpc = RpcProxy(USER)
    # admin_rpc = RpcProxy(ADMIN)
    


    #@rpc
    def login(self, username, password):
        returned_data = {}
        # returned_data[IS_ADMIN] = self.admin_rpc.check_is_admin_existed(username)

        call_str = "admin.check_is_admin_existed('%s')" % (username)
        returned_data[IS_ADMIN] = eval(admin_client.call(call_str))

        if returned_data[IS_ADMIN]:
            # result, msg, account_id = self.admin_rpc.verify_login_input(username, password)
            call_str = "admin.verify_login_input('%s', '%s')" % (username, password)
            result, msg, account_id = eval(admin_client.call(call_str))
        else:
            # result, msg, account_id = self.user_rpc.verify_login_input(username, password)
            call_str = "user.verify_login_input('%s', '%s')" % (username, password)
            result, msg, account_id = eval(user_client.call(call_str))

        returned_data[ID] = account_id
        returned_data[MESSAGE] = msg
        return result, returned_data


    #@rpc
    def register(self, username, first_name, last_name, password, date_joined, is_admin):
        if is_admin:
            # return self.admin_rpc.create_admin_account(username, password, first_name, last_name, date_joined)
            call_str = "admin.create_admin_account('%s', '%s', '%s', '%s', '%s')" % (username, password, first_name, last_name, date_joined)
            return eval(admin_client.call(call_str))
        # return self.user_rpc.create_account(username, password, first_name, last_name, date_joined)
        call_str = "user.create_account('%s', '%s', '%s', '%s', '%s')" % (username, password, first_name, last_name, date_joined)
        return eval(user_client.call(call_str))


    #@rpc
    def get_account_info(self, account_id):
        # result, data = self.user_rpc.get_account_info(account_id)
        call_str = "user.get_account_info(%d)" % (account_id)
        result, data = eval(user_client.call(call_str))

        if not result:
            # result, data = self.admin_rpc.get_account_info(account_id)
            call_str = "admin.get_account_info(%d)" % (account_id)
            result, data = eval(admin_client.call(call_str))
        return result, data


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

login = Login()
print(" [x] Awaiting RPC requests")

channel = getRpcChannel([LOGIN])
channel.start_consuming()


