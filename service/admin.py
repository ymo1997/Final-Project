from config import *

#---------- CONFIG ----------#
admin_db = client.admin_db
admin_col = admin_db.admin


#---------- DATA MODEL ----------#
ID = "_id"
ADMIN = "admin"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
PASSWORD = "password"
DATE_JOINED = "date_joined"
IS_ADMIN = "is_admin"


class Admin(object):
    name = ADMIN

    user_rpc = RpcProxy(USER)
    search_rpc = RpcProxy(SEARCH)

    def __init__(self):
        self.next_new_account_id = self.get_last_id() + 1


    @rpc
    def check_is_admin_existed(self, admin):
        condition = {ADMIN: admin}
        return admin_col.find_one(condition) is not None


    def verify_password(self, admin, password):
        condition = {ADMIN: admin}
        result = admin_col.find_one(condition)
        return result[PASSWORD] == password


    @rpc
    def verify_login_input(self, admin, password):
        if self.check_is_admin_existed(admin):
            account_id = self.get_account_id(admin)
            if self.verify_password(admin, password):
                return True, admin_verify_login_input_suceeded, account_id
            else:
                return False, admin_verify_login_input_failed_wrong_password, account_id
        else:
            return False, admin_verify_login_input_failed_invalid_admin, None


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
        return self.user_rpc.suspend_account(username = username)


    @rpc
    def create_user_account(self, username, password, first_name, last_name, date_joined):
        return self.user_rpc.create_account(username, password, first_name, last_name, date_joined)


    @rpc
    def delete_user_account(self, username):
        return self.user_rpc.delete_account(username = username)


    @rpc
    def update_user_account_info(self, account_id, username, password, first_name, last_name):
        return self.user_rpc.update_account_info(account_id, username, password, first_name, last_name)


    def check_is_account_id_existed(self, account_id):
        condition = {ID: account_id}
        return admin_col.find_one(condition) is not None


    def insert_admin_db(self, record):
        try:
            admin_col.insert_one(record)
            return True
        except Exception as e:
            logging.error("%s: Exception occurred while insert record in db :: %s" % (__name__, e))
            return False 


    def get_account_id(self, admin):
        condition = {ADMIN: admin}
        result = admin_col.find_one(condition)
        return result[ID]


    def delete_admin_db(self, condition):
        result = admin_col.delete_one(condition)
        return result.deleted_count > 0


    def get_last_id(self):
        last_account = admin_col.find().sort(ID, -1).limit(1)
        if last_account.count() > 0:
            return last_account[0][ID]

