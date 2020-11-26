import pytest
from requests import post, get

server_url = 'http://localhost:5000'

def test_user_create_account():
    params = {
        'username': 'Johnson', 
        'password': 'JOHNSON'
    }
    api_url = server_url + '/user/create-account'

    response = post(api_url, json = params)
    assert response.status_code == 200

    response = post(api_url, json = params)
    assert response.status_code == 400


def test_user_info_edit():
    params = {
        'username': 'Johnson', 
        'sex': 'male',
        'age': 60
    }
    api_url = server_url + '/user/update-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_user_delete():
    params = {
        'username': 'Johnson', 
        'password': 'JOHNSON'
    }
    api_url = server_url + '/user/delete-account'

    response = post(api_url, json = params)
    assert response.status_code == 200
    
    response = post(api_url, json = params)
    assert response.status_code == 400


