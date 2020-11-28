from responses import *
from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime


#---------- DATABASES ----------#
client = MongoClient('localhost:27017')

def getDatabaseCusor(dbname):
	connect = psycopg2.connect(
    	user = "dbuser", password = "guest", host = "localhost", port = "5432", database = dbname + "_db"
	)
	connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	return connect.cursor()



#---------- SERVICES ----------#
ADMIN = "admin"
USER = "user"
AUCTION = "auction"
ITEM = "item"
SEARCH = "search"
LOGIN = "login"
NOTIFICATION = "notification"
SHOPPING_CART = "shopping_cart"
