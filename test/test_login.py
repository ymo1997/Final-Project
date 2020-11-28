import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'


def test_login():
    params = {
        'email': 'Yueyang@mail.com',
        'password': 'Zhang'
    }
    api_url = server_url + '/login/login'

    response = post(api_url, json = params)
    assert response.status_code == 200
    assert response.json()["_id"] == 10001
    assert response.json()["is_admin"] == True

    params = {
        'email': 'amy@mail.com',
        'password': 'AMY'
    }
    api_url = server_url + '/login/login'

    response = post(api_url, json = params)
    assert response.status_code == 200
    assert response.json()["_id"] == 1
    assert response.json()["is_admin"] == False

    params = {
        'email': 'amy@mail.com',
        'password': 'JOHN'
    }
    api_url = server_url + '/login/login'

    response = post(api_url, json = params)
    assert response.status_code == 400
    assert response.json()["_id"] == 1
    assert response.json()["is_admin"] == False

    params = {
        'email': 'ashley@mail.com',
        'password': 'JOHN'
    }
    api_url = server_url + '/login/login'

    response = post(api_url, json = params)
    assert response.status_code == 400
    assert response.json()["_id"] == None
    assert response.json()["is_admin"] == False


def test_get_account_info():
    params = {
        'account_id': 1
    }

    api_url = server_url + '/login/get-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200
    assert response.json()['email'] == 'amy@mail.com'

    params = {
        'account_id': 10001
    }

    api_url = server_url + '/login/get-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200
    assert response.json()['email'] == 'Yueyang@mail.com'


def test_register():
    params = {
        'email': 'sherlock@mail.com',
        'password': 'Zhang', 
        'first_name': 'a',
        'last_name': 'b',
        'is_admin': True
    }
    api_url = server_url + '/login/register'

    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'email': 'sherlock@mail.com'
    }
    api_url = server_url + '/admin/delete-admin-account'
    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'email': 'zackerburg@mail.com',
        'password': 'Zhang', 
        'first_name': 'a',
        'last_name': 'b',
        'is_admin': False
    }
    api_url = server_url + '/login/register'

    response = post(api_url, json = params)
    assert response.status_code == 200
    newly_created_user_id = response.json()["_id"]
    
    params = {
        "email": 'zackerburg@mail.com'
    }
    api_url = server_url + '/admin/delete-user-account'
    esponse = post(api_url, json = params)
    assert response.status_code == 200
