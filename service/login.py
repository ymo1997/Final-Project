from config import *

#---------- DATA MODEL ----------#
IS_ADMIN = "is_admin"
ID = "_id"

MESSAGE = "msg"

class Login(object):
    name = LOGIN

    user_rpc = RpcProxy(USER)
    admin_rpc = RpcProxy(ADMIN)


    @rpc
    def login(self, username, password):
        returned_data = {}
        returned_data[IS_ADMIN] = self.admin_rpc.check_is_admin_existed(username)

        if returned_data[IS_ADMIN]:
            result, msg, account_id = self.admin_rpc.verify_login_input(username, password)
        else:
            result, msg, account_id = self.user_rpc.verify_login_input(username, password)
        returned_data[ID] = account_id
        returned_data[MESSAGE] = msg
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


