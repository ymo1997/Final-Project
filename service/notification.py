from mailjet_rest import Client
from config import *

API_KEY = '01c8781e582ce292c1db9fae3d494c1c'
API_SECRET = 'caa00a1184d5714ad2066663fb1aa789'
SENDER_EMAIL = 'yinghuamo.4174@gmail.com'

# https://www.mailjet.com/
mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')

class Notification(object):
    name = NOTIFICATION

    # @rpc
    def send_email(self, email_address, subject, content):
        api_key = API_KEY
        api_secret = API_SECRET
        data = {
          'Messages': [
            {
              "From": {
                "Email": SENDER_EMAIL,
                "Name": ""
              },
              "To": [
                {
                  "Email": email_address,
                  "Name": ""
                }
              ],
              "Subject": subject,
              "TextPart": content,
              "HTMLPart": "",
              "CustomID": "AppGettingStartedTest"
            }
          ]
        }
        result = mailjet.send.create(data=data)
        return True, result.json()



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


notification = Notification()

print(" [x] Awaiting RPC requests")

channel = getRpcChannel([NOTIFICATION, ITEM + "_" + NOTIFICATION])
channel.start_consuming()

