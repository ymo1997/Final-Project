import pytest
import requests

server_address = "http://localhost:5000/"

def test_admin_user_create():
    test_username = "Johnson"
    test_password = "JOHNSON"
    test_json = {"username" : test_username, "password" : test_password}
    test_response = requests.post(server_address + "admin-user-create", json = test_json)
    assert test_response.status_code == 200
    test_response = requests.post(server_address + "admin-user-create", json = test_json)
    assert test_response.status_code == 400

def test_admin_user_info_edit():
    test_username = "Johnson"
    sex = "male"
    age = 60
    test_json = {"username" : test_username, "sex" : sex, "age": age}
    test_response = requests.post(server_address + "admin-user-info-edit", json = test_json)
    assert test_response.status_code == 200

def test_admin_user_suspend():
    test_username = "Johnson"
    test_json = {"username" : test_username}
    test_response = requests.post(server_address + "admin-user-suspend", json = test_json)
    assert test_response.status_code == 200

def test_admin_user_delete():
    test_username = "Johnson"
    test_json = {"username" : test_username}
    test_response = requests.post(server_address + "admin-user-delete", json = test_json)
    assert test_response.status_code == 200
    test_response = requests.post(server_address + "admin-user-delete", json = test_json)
    assert test_response.status_code == 400




