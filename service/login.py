from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient

class Login(object):
    name = "login"

    user_rpc = RpcProxy("user")
    admin_rpc = RpcProxy("admin")


    @rpc
    def login(self, username, password):
        returned_data = {}
        returned_data["is_admin"] = self.admin_rpc.check_is_admin_existed(username)

        if returned_data["is_admin"]:
            result, msg, account_id = self.admin_rpc.verify_login_input(username, password)
        else:
            result, msg, account_id = self.user_rpc.verify_login_input(username, password)
        returned_data["_id"] = account_id
        returned_data["msg"] = msg
        return result, returned_data


    @rpc
    def register(self, username, first_name, last_name, password, date_joined, is_admin):
        if is_admin:
            return self.admin_rpc.create_admin_account(username, password, first_name, last_name, date_joined)
        return self.user_rpc.create_account(username, password, first_name, last_name, date_joined)


    @rpc
    def get_account_info(self, account_id):
        result, data = self.user_rpc.get_account_info(account_id)
        if not result:
            result, data = self.admin_rpc.get_account_info(account_id)
        return result, data


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
