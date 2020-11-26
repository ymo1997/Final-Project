from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient
from responses import *

#---------- DATA MODEL ----------#
ID = "_id"
ADMIN = "admin"
PASSWORD = "password"

#---------- CONFIG ----------#
server_name = "admin"

client = MongoClient('localhost:27017')
admin_db = client.admin_db
admin_col = admin_db.admin

class Admin(object):

    name = server_name

    user_rpc = RpcProxy("user")
    search_rpc = RpcProxy("search")


    @rpc
    def login(self, admin, password):
        if self.check_is_admin_existed(admin):
            if self.verifyPassword(admin, password):
                return True, admin_verify_login_input_suceeded
            else:
                return False, admin_verify_login_input_failed_wrong_password
        else:
            return False, admin_verify_login_input_failed_invalid_admin


    @rpc
    def suspend_user_account(self, username):
        return self.user_rpc.suspend_account(username)


    @rpc
    def create_user_account(self, username, password):
        return self.user_rpc.create_account(username, password)


    @rpc
    def delete_user_account(self, username):
        return self.user_rpc.delete_account(username, "", True)


    @rpc
    def update_user_account_info(self, username, sex, age):
        return self.user_rpc.update_account_info(username, sex, age)


    # TODO
    @rpc
    def search_user(self, keyword):
        return self.search_rpc.search_user(keyword)


    def check_is_admin_existed(self, admin):
        condition = {ADMIN: admin}
        return admin_col.find_one(condition) is not None


    def verifyPassword(self, admin, password):
        condition = {ADMIN: admin}
        result = admin_col.find_one(condition)
        return result[PASSWORD] == password

