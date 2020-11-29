from config import *

#---------- CONFIG ----------#
user_db = client.user_db
user_col = user_db.user


#---------- DATA MODEL ----------#
ID = "_id"
USERNAME = "username"
PASSWORD = "password"
STATUS = "status"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
DATE_JOINED = "date_joined"
IS_ADMIN = "is_admin"
SEX = "sex"
AGE = "age"
CREDIT = "credit"

STATUS_VALID = "valid"
STATUS_INVALID = "invalid"

NOT_FILLED = "not_filled"


class User(object):
    name = USER
    shopping_cart_rpc = RpcProxy(SHOPPING_CART)
    item_rpc = RpcProxy(ITEM)


    def __init__(self):                                                 
        self.next_new_account_id = self.get_last_id() + 1


    @rpc
    def create_account(self, username, password, first_name, last_name, date_joined):
        returned_data = {ID: None, MESSAGE: None}
        if self.check_is_username_existed(username):
            returned_data[MESSAGE] = user_create_account_failed
            return False, returned_data

        new_record = {
            ID: self.next_new_account_id, 
            USERNAME: username, 
            PASSWORD: password, 
            STATUS: STATUS_VALID, 
            FIRST_NAME: first_name, 
            LAST_NAME: last_name, 
            DATE_JOINED: date_joined
        }

        self.insert_user_db(new_record)
        returned_data[MESSAGE] = user_create_account_suceeded
        returned_data[ID] = self.next_new_account_id

        self.shopping_cart_rpc.create_user_shopping_cart(self.next_new_account_id)
        self.next_new_account_id += 1

        return True, returned_data


    @rpc
    def update_account_info(self, account_id, username, password, first_name, last_name):
        condition = {ID: account_id}
        record = user_col.find_one(condition)
        if record == None:
            return False, user_update_account_info_failed
        record[USERNAME] = username
        record[PASSWORD] = password
        record[FIRST_NAME] = first_name
        record[LAST_NAME] = last_name
        result = user_col.update_one(condition, {'$set': record})

        if result.modified_count == 0:
            return False, user_update_account_info_failed
        else:
            return True, user_update_account_info_suceeded



    @rpc
    def delete_account(self, account_id = None, username = None):
        if username is not None:
            if self.check_is_username_existed(username):
                account_id = self.get_account_id(username)
            else:
                return False, user_delete_account_failed_not_existed

        condition = {ID: account_id}
        if self.delete_user_db(condition):
            self.shopping_cart_rpc.delete_user_shopping_cart(account_id)
            self.item_rpc.delete_user_sell_items(account_id)
            return True, user_delete_account_suceeded
        else:
            return False, user_delete_account_failed_db
    

    @rpc
    def suspend_account(self, account_id = None, username = None):
        if username is not None:
            if self.check_is_username_existed(username):
                account_id = self.get_account_id(username)
            else:
                return False, user_suspend_account_failed

        condition = {ID: account_id}
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
            account_id = self.get_account_id(username)
            result, returned_data = self.get_account_info(account_id)
            if result:
                status = returned_data[STATUS]
                if status == STATUS_INVALID:
                    return False, user_verify_login_input_failed_invalid_username, None
                if self.verify_password(username, password):
                    return True, user_verify_login_input_suceeded, account_id
                else:
                    return False, user_verify_login_input_failed_wrong_password, account_id
        else:
            return False, user_verify_login_input_failed_invalid_username, None


    @rpc
    def get_account_info(self, account_id):
        condition = {ID: account_id}
        returned_data = user_col.find_one(condition)
        if returned_data is not None:
            returned_data[IS_ADMIN] = False
            returned_data[MESSAGE] = user_get_account_info_suceeded
            return True, returned_data
        else:
            returned_data = {MESSAGE: user_get_account_info_failed}
            return False, returned_data

    

    def delete_user_db(self, condition):
        result = user_col.delete_one(condition)
        return result.deleted_count > 0


    def insert_user_db(self, record):
        try:
            user_col.insert_one(record)
            return True
        except Exception as e:
            logging.error("%s: Exception occurred while insert record in db :: %s" % format(__name__, e))
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

    def check_is_account_id_existed(self, account_id):
        condition = {ID: account_id}
        return user_col.find_one(condition) is not None
        

    def get_last_id(self):
        last_account = user_col.find().sort(ID, -1).limit(1)
        if last_account.count() > 0:
            return last_account[0][ID]


