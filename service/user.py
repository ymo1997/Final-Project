from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient
from responses import *

#---------- DATA MODEL ----------#
ID = "_id"
USERNAME = "email"
PASSWORD = "password"
STATUS = "status"
SEX = "sex"
AGE = "age"
CREDIT = "credit"

STATUS_VALID = "valid"
STATUS_INVALID = "invalid"

NOT_FILLED = "not_filled"

#---------- CONFIG ----------#
server_name = "user"

client = MongoClient('localhost:27017')
user_db = client.user_db
user_col = user_db.user

class User(object):
    name = server_name
    shopping_cart_rpc = RpcProxy("shopping_cart")


    def __init__(self):
        self.next_new_account_id = self.get_last_id() + 1


    @rpc
    def create_account(self, username, password):
        if self.check_is_username_existed(username):
            return False, user_create_account_failed

        new_record = {
            ID: self.next_new_account_id, 
            USERNAME: username, 
            PASSWORD: password, 
            STATUS: STATUS_VALID, 
            SEX: NOT_FILLED, 
            AGE: -1, 
            CREDIT: 0
        }

        self.insert_user_db(new_record)

        self.shopping_cart_rpc.create_user_shopping_cart(self.next_new_account_id)
        self.next_new_account_id += 1
        return True, user_create_account_suceeded


    @rpc
    def update_account_info(self, username, sex, age):
        if self.check_is_username_existed(username):
            condition = {USERNAME: username}
            record = user_col.find_one(condition)
            record[SEX] = sex
            record[AGE] = age
            result = user_col.update_one(condition, {'$set': record})

            if result.modified_count == 0:
                return False, user_update_account_info_failed
            else:
                return True, user_update_account_info_suceeded


    @rpc
    def delete_account(self, username, password, isAdmin = False):
        if self.check_is_username_existed(username):
            account_id = self.get_account_id(username)
            if self.verify_password(username, password) or isAdmin:
                condition = {USERNAME: username}
                if self.delete_user_db(condition):
                    self.shopping_cart_rpc.delete_user_shopping_cart(account_id)
                    return True, user_delete_account_suceeded
                else:
                    return False, user_delete_account_failed_db
        else:
            return False, user_delete_account_failed_not_existed
    

    @rpc
    def suspend_account(self, username):
        condition = {USERNAME: username}
        record = user_col.find_one(condition)
        record[STATUS] = STATUS_INVALID
        result = user_col.update_one(condition, {'$set': record})

        if result.modified_count == 0:
            return False, user_suspend_account_failed
        else:
            return True, user_suspend_account_suceeded


    @rpc
    def verify_login_input(self, username, password):
        if self.check_is_username_existed(username):
            if self.verify_password(username, password):
                return True, user_verify_login_input_suceeded
            else:
                return False, user_verify_login_input_failed_wrong_password
        else:
            return False, user_verify_login_input_failed_invalid_username
    

    def delete_user_db(self, condition):
        result = user_col.delete_one(condition)
        return result.deleted_count > 0


    def insert_user_db(self, record):
        try:
            user_col.insert_one(record)
            return True
        except Exception as e:
            logging.error("An exception occurred while insert record in db :: {}".format(e))
            return False


    def verify_password(self, username, password):
        condition = {USERNAME: username}
        result = user_col.find_one(condition)
        return result[PASSWORD] == password


    def get_account_id(self, username):
        condition = {USERNAME: username}
        result = user_col.find_one(condition)
        return result[ID]


    def check_is_username_existed(self, username):
        condition = {USERNAME: username}
        return user_col.find_one(condition) is not None
        

    def get_last_id(self):
        last_account = user_col.find().sort('_id', -1).limit(1)
        if last_account.count() > 0:
            return last_account[0][ID]


