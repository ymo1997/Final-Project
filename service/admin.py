from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient
from responses import *

#---------- DATA MODEL ----------#
ID = "_id"
ADMIN = "admin"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
PASSWORD = "password"
DATE_JOINED = "date_joined"
IS_ADMIN = "is_admin"


#---------- CONFIG ----------#
server_name = "admin"

client = MongoClient('localhost:27017')
admin_db = client.admin_db
admin_col = admin_db.admin

class Admin(object):

    name = server_name

    user_rpc = RpcProxy("user")
    search_rpc = RpcProxy("search")

    def __init__(self):
        self.next_new_account_id = self.get_last_id() + 1


    @rpc
    def verify_login_input(self, admin, password):
        if self.check_is_admin_existed(admin):
            if self.verify_password(admin, password):
                return True, admin_verify_login_input_suceeded
            else:
                return False, admin_verify_login_input_failed_wrong_password
        else:
            return False, admin_verify_login_input_failed_invalid_admin

    @rpc
    def create_admin_account(self, admin, password, first_name, last_name, date_joined):
        returned_data = {ID: None, MESSAGE: None}
        if self.check_is_admin_existed(admin):
            returned_data[MESSAGE] = admin_create_account_failed
            return False, returned_data

        new_record = {
            ID: self.next_new_account_id, 
            ADMIN: admin, 
            PASSWORD: password, 
            FIRST_NAME: first_name, 
            LAST_NAME: last_name, 
            DATE_JOINED: date_joined
        }

        self.insert_admin_db(new_record)
        returned_data[MESSAGE] = admin_create_account_suceeded
        returned_data[ID] = self.next_new_account_id

        self.next_new_account_id += 1

        return True, returned_data


    @rpc
    def delete_admin_account(self, admin):
        if self.check_is_admin_existed(admin):
            condition = {ADMIN: admin}
            if self.delete_admin_db(condition):
                return True, admin_delete_admin_account_suceeded
            else:
                return False, admin_delete_admin_account_failed_db
        else:
            return False, admin_delete_admin_account_failed_not_existed


    @rpc
    def get_account_info(self, account_id):
        condition = {ID: account_id}
        returned_data = admin_col.find_one(condition)
        if returned_data is not None:
            returned_data[IS_ADMIN] = True
            returned_data[MESSAGE] = admin_get_account_info_suceeded
            return True, returned_data
        else:
            returned_data = {MESSAGE: admin_get_account_info_failed}
            return False, returned_data


    @rpc
    def suspend_user_account(self, username):
        return self.user_rpc.suspend_account(username)


    @rpc
    def create_user_account(self, username, password, first_name, last_name, date_joined):
        return self.user_rpc.create_account(username, password, first_name, last_name, date_joined)


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

    @rpc
    def check_is_admin_existed(self, admin):
        condition = {ADMIN: admin}
        return admin_col.find_one(condition) is not None


    def verify_password(self, admin, password):
        condition = {ADMIN: admin}
        result = admin_col.find_one(condition)
        return result[PASSWORD] == password


    def insert_admin_db(self, record):
        try:
            admin_col.insert_one(record)
            return True
        except Exception as e:
            logging.error("An exception occurred while insert record in db :: {}".format(e))
            return False 

    def delete_admin_db(self, condition):
        result = admin_col.delete_one(condition)
        return result.deleted_count > 0

    def get_last_id(self):
        last_account = admin_col.find().sort(ID, -1).limit(1)
        if last_account.count() > 0:
            return last_account[0][ID]

