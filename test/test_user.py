import pytest
import sys
sys.path.append("..")
from service.user import User

user_rpc = User()

def test_user_register():
    test_username = "Johnson"
    test_password = "JOHNSON"
    result, _ = user_rpc.register(test_username, test_password)
    assert result == True
    result, _ = user_rpc.register(test_username, test_password)
    assert result == False

def test_user_info_edit():
    test_username = "Johnson"
    sex = "male"
    age = 60
    result, _ = user_rpc.edit_user_info(test_username, sex, age)
    assert result == True

def test_user_delete():
    test_username = "Johnson"
    test_password = "JOHNSON"
    result, _ = user_rpc.delete_user(test_username, test_password)
    assert result == True
    result, _ = user_rpc.delete_user(test_username, test_password)
    assert result == False

