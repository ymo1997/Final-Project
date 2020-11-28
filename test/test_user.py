import pytest
from requests import post, get

server_url = 'http://localhost:5000'

def pytest_namespace():
    return {
        'newly_created_user_id': None
        }

def test_user_create_account():
    params = {
        'email': 'Johnson@mail.com', 
        'password': 'JOHNSON',
        'first_name': 'Boris',
        'last_name':'Johnson',
    }
    api_url = server_url + '/user/create-account'

    response = post(api_url, json = params)
    pytest.newly_created_user_id = response.json()["_id"]
    assert response.status_code == 200

    response = post(api_url, json = params)
    assert response.status_code == 400


def test_user_info_edit():
    params = {
        'account_id': pytest.newly_created_user_id, 
        'email': 'Johnson@mail.com', 
        'password': "JOHNSON", 
        'first_name': 'Jack', 
        'last_name': 'Biden',
    }
    api_url = server_url + '/user/update-account-info'

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


def test_user_suspend():
    params = {
        'account_id': pytest.newly_created_user_id
    }
    api_url = server_url + '/user/suspend-account'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_user_delete():
    params = {
        'account_id': pytest.newly_created_user_id
    }
    api_url = server_url + '/user/delete-account'

    response = post(api_url, json = params)
    assert response.status_code == 200
    
    response = post(api_url, json = params)
    assert response.status_code == 400


