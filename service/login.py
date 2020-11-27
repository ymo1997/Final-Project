from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient

class Login(object):
    name = "login"

    user_rpc = RpcProxy("user")
    admin_rpc = RpcProxy("admin")


    @rpc
    def login(self, email, password):
        returned_data = {}
        returned_data["is_admin"] = self.admin_rpc.check_is_admin_existed(email)

        if returned_data["is_admin"]:
            result, msg = self.admin_rpc.login(email, password)
        else:
            result, msg = self.user_rpc.verify_login_input(email, password)
            
        returned_data["msg"] = msg
        return result, returned_data

    @rpc
    def user_login(self, email, password):
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
