import pytest
from requests import post, get

server_url = 'http://localhost:5000'

def pytest_namespace():
    return {
        'newly_created_admin_id': None,
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

    response = post(api_url, json = params)
    assert response.status_code == 400


def test_admin_update_user_account_info():
    params = {
        'email': 'Johnson@mail.com', 
        'sex': 'male',
        'age': 60
    }
    api_url = server_url + '/admin/update-user-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200


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



