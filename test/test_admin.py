import pytest
from requests import post, get

server_url = 'http://localhost:5000'

def test_admin_create_user_account():
    params = {
        'username': 'Johnson', 
        'password': 'JOHNSON'
    }
    api_url = server_url + '/admin/create-user-account'

    response = post(api_url, json = params)
    assert response.status_code == 200

    response = post(api_url, json = params)
    assert response.status_code == 400


def test_admin_update_user_account_info():
    params = {
        'username': 'Johnson', 
        'sex': 'male',
        'age': 60
    }
    api_url = server_url + '/admin/update-user-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_admin_suspend_user_account():
    params = {
        'username': 'Johnson'
    }
    api_url = server_url + '/admin/suspend-user-account'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_admin_user_delete():
    params = {
        'username': 'Johnson',
    }
    api_url = server_url + '/admin/delete-user-account'

    response = post(api_url, json = params)
    assert response.status_code == 200
    
    response = post(api_url, json = params)
    assert response.status_code == 400




