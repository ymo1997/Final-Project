import pytest
from requests import post, get

server_url = 'http://localhost:5000'

def pytest_namespace():
    return {
        'newly_created_admin_id': None,
        'newly_created_user_id': None
        }

def test_admin_create_admin_account():
    params = {
        'email': 'Johnson@mail.com', 
        'password': 'JOHNSON',
        'first_name': 'Boris',
        'last_name':'Johnson',
    }
    api_url = server_url + '/admin/create-admin-account'

    response = post(api_url, json = params)
    assert response.status_code == 200


    response = post(api_url, json = params)
    assert response.status_code == 400


def test_admin_delete_admin_account():
    params = {
        'email': 'Johnson@mail.com', 
    }
    api_url = server_url + '/admin/delete-admin-account'

    response = post(api_url, json = params)
    assert response.status_code == 200

    response = post(api_url, json = params)
    assert response.status_code == 400


def test_admin_create_user_account():
    params = {
        'email': 'Johnson@mail.com', 
        'password': 'JOHNSON',
        'first_name': 'Boris',
        'last_name':'Johnson',
    }
    api_url = server_url + '/admin/create-user-account'

    response = post(api_url, json = params)
    assert response.status_code == 200
    pytest.newly_created_user_id = response.json()["_id"]

    response = post(api_url, json = params)
    assert response.status_code == 400


def test_admin_update_user_account_info():
    params = {
        'account_id': pytest.newly_created_user_id, 
        'email': 'Johnson@mail.com', 
        'password': "JOHNSON", 
        'first_name': 'Jack', 
        'last_name': 'Biden',
    }
    api_url = server_url + '/admin/update-user-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'account_id': pytest.newly_created_user_id
    }

    api_url = server_url + '/login/get-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200
    assert response.json()['email'] == 'Johnson@mail.com'
    assert response.json()['first_name'] == 'Jack'
    assert response.json()['last_name'] == 'Biden'


def test_admin_suspend_user_account():
    params = {
        'email': 'Johnson@mail.com'
    }
    api_url = server_url + '/admin/suspend-user-account'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_admin_user_delete():
    params = {
        'email': 'Johnson@mail.com',
    }
    api_url = server_url + '/admin/delete-user-account'

    response = post(api_url, json = params)
    assert response.status_code == 200
    
    response = post(api_url, json = params)
    assert response.status_code == 400



