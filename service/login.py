from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient

class Login(object):
    name = "login"

    @rpc
    def user_login(self, username, password):
    	return True, ""

    @rpc
    def admin_login(self, admin, password):
    	return True, ""

    @rpc
    def user_logout(self, username, password):
    	return True, ""
    	
    @rpc
    def admin_logout(self, admin, password):
    	return True, ""
