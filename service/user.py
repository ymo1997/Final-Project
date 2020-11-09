from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient

client = MongoClient('localhost:27017')
user_db = client.user_db
user_col = user_db.user

# Data Model
ID = "_id"
USERNAME = "username"
PASSWORD = "password"
STATUS = "status"
SEX = "sex"
AGE = "age"
CREDIT = "credit"

class User(object):
    name = "user"

    @rpc
    def register(self, username, password):
        if self.isUsernameExisted(username):
            return False, "Failed: Username exists."
        new_record = {ID: user_col.count_documents({}) + 1, USERNAME: username, PASSWORD: password, STATUS: "valid", SEX: "female", AGE: 20, CREDIT: 1000}
        self.insert_user_db(new_record)
        return True, "Suceeded: User created."

    @rpc
    def validate_login(self, username, password):
        if self.isUsernameExisted(username):
            if self.verifyPassword(username, password):
                return True, "Suceeded: User {} password matches.".format(username)
            else:
                return False, "Failed: Wrong password."
        else:
            return False, "Failed: Invalid username."

    @rpc
    def logout(self, username):
        return True, "Suceeded: {} logout Successfully.".format(username)

    @rpc
    def suspend_user(self, username):
        condition = {USERNAME: username}
        record = user_col.find_one(condition)
        record[STATUS] = 'invalid'
        result = user_col.update_one(condition, {'$set': record})
        if result.modified_count == 0:
            return False, "Failed: User {} was not modified.".format(username)
        else:
            return True, "Suceeded: User {} is now invalid".format(username)

    @rpc
    def delete_user(self, username, password, isAdmin = False):
        if self.isUsernameExisted(username):
            if self.verifyPassword(username, password) or isAdmin:
                condition = {USERNAME: username}
                if self.delete_user_db(condition):
                    return True, "Suceeded: User deleted."
                else:
                    return False, "Failed: User was failed to be deleted in db."
        else:
            return False, "Failed, User doesn't exist."

    @rpc
    def edit_user_info(self, username, sex, age):
        if self.isUsernameExisted:
            condition = {USERNAME: username}
            record = user_col.find_one(condition)
            record[SEX] = sex
            record[AGE] = age
            result = user_col.update_one(condition, {'$set': record})
            if result.modified_count == 0:
                return False, "Failed: User info {} not changed.".format(username)
            else:
                return True, "Suceeded: User info {} changed".format(username)


    def delete_user_db(self, condition):
        result = user_col.delete_one(condition)
        return result.deleted_count > 0

    def insert_user_db(self, record):
        try:
            user_col.insert_one(record)
            return True
        except Exception as e:
            print("An exception occurred while insert record in db ::", e)
            return False

    def verifyPassword(self, username, password):
        condition = {USERNAME: username}
        result = user_col.find_one(condition)
        return result[PASSWORD] == password

    def isUsernameExisted(self, username):
        condition = {USERNAME: username}
        return user_col.find_one(condition) is not None





