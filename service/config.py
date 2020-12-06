from responses import *
# from nameko.rpc import rpc, RpcProxy
# from nameko.standalone.rpc import ClusterRpcProxy
from pymongo import MongoClient, ASCENDING
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
import pika
import uuid


#---------- RABBITMQ ----------#
rabbit_address = '172.17.0.2'
rpc_queue_name_prefix = 'rpc_queue_'
prefetch_count = 1

class RPCClient:
    def __init__(self, queue_name):
      self.queue_name = queue_name
      params = pika.ConnectionParameters(host=rabbit_address, heartbeat=0)
      self.connection = pika.BlockingConnection(params)
      self.channel = self.connection.channel()
      result = self.channel.queue_declare(
          queue = str(uuid.uuid4()), 
          exclusive=True
      )
      self.callback_queue = result.method.queue
      self.channel.basic_consume(
          queue = self.callback_queue,
          on_message_callback = self.on_response
      )
         
    def call(self, n):
      self.response = None

      self.corr_id = str(uuid.uuid4())
      self.channel.basic_publish(
          exchange = '',
          routing_key = rpc_queue_name_prefix + self.queue_name,
          properties=pika.BasicProperties(
              correlation_id=self.corr_id,
              reply_to=self.callback_queue
          ),
          body = n
      )

      while self.response is None:
          self.connection.process_data_events()

      return self.response
 
    def on_response(self, ch, method, props, body):
      if(self.corr_id == props.correlation_id):
        self.response = body


class RPCAsyncClient:
    def __init__(self, queue_name):
      self.queue_name = queue_name
      params = pika.ConnectionParameters(host=rabbit_address, heartbeat=0)
      self.connection = pika.BlockingConnection(params)
      self.channel = self.connection.channel()
      result = self.channel.queue_declare(
          queue = str(uuid.uuid4()), 
          exclusive=True
      )
      self.callback_queue = result.method.queue
      self.channel.basic_consume(
          queue = self.callback_queue,
          on_message_callback = self.on_response
      )
         
    def call(self, n):
      self.response = None

      self.corr_id = str(uuid.uuid4())
      self.channel.basic_publish(
          exchange = '',
          routing_key = rpc_queue_name_prefix + self.queue_name,
          properties=pika.BasicProperties(
              correlation_id=self.corr_id,
              reply_to=self.callback_queue
          ),
          body = n
      )

      return self.response
 
    def on_response(self, ch, method, props, body):
      if(self.corr_id == props.correlation_id):
        self.response = body





#---------- DATABASES ----------#
client = MongoClient('localhost:27017')

def getDatabaseCusor(dbname):
	connect = psycopg2.connect(
    	user = "dbuser", password = "guest", host = "localhost", port = "5432", database = dbname + "_db"
	)
	connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	return connect.cursor()



#---------- SERVICES ----------#
# CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}
# rpc = ClusterRpcProxy(CONFIG)

ADMIN = "admin"
USER = "user"
AUCTION = "auction"
ITEM = "item"
SEARCH = "search"
LOGIN = "login"
NOTIFICATION = "notification"
SHOPPING_CART = "shopping_cart"


#---------- CONTAINERS ----------#
# docker run -it -d --rm --name item_service -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  service_container
# docker run -it -d --rm --name user_service -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  service_container
# docker run -it -d --rm --name shopping_cart_service -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  service_container
# docker run -it -d --rm --name search_service -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  service_container
# docker run -it -d --rm --name notification_service -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  service_container
# docker run -it -d --rm --name auction_service -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  service_container
# docker run -it -d --rm --name admin_service -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  service_container
# docker run -it -d --rm --name login_service -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  service_container
# docker exec -it item_service bash
# docker exec -it user_service bash
# docker exec -it shopping_cart_service bash
# docker exec -it search_service bash
# docker exec -it notification_service bash
# docker exec -it auction_service bash
# docker exec -it admin_service bash
# docker exec -it login_service bash
# python3 final_project/service/
# docker run -it -d --rm --name apis -e POSTGRES_USER=dbuser -e POSTGRES_DB=testdb  -e POSTGRES_PASSWORD=guest -p 5000:5000 -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project  postgresql



# docker run -di -P --name user_service_new -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project service_clean
# docker run -di -P --name item_service_new -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project service_clean
# docker run -di -P --name auction_service_new -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project service_clean
# docker run -di -P --name shopping_cart_service_new -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project service_clean
# docker run -di -P --name search_service_new -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project service_clean
# docker run -di -P --name notification_service_new -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project service_clean
# docker run -di -P --name admin_service_new -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project service_clean
# docker run -di -P --name login_service_new -v /Users/yinghuamo/Documents/GitHub/Final-Project:/final_project service_clean
# docker exec -it item_service_new bash
# docker exec -it user_service_new bash
# docker exec -it shopping_cart_service_new bash
# docker exec -it search_service_new bash
# docker exec -it notification_service_new bash
# docker exec -it auction_service_new bash
# docker exec -it admin_service_new bash
# docker exec -it login_service_new bash
