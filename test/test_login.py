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
    assert response.json()["is_admin"] == True

    params = {
        'email': 'amy@mail.com',
        'password': 'AMY'
    }
    api_url = server_url + '/login/login'

    response = post(api_url, json = params)
    assert response.status_code == 200
    assert response.json()["is_admin"] == False

    params = {
        'email': 'amy@mail.com',
        'password': 'JOHN'
    }
    api_url = server_url + '/login/login'

    response = post(api_url, json = params)
    assert response.status_code == 400
    assert response.json()["is_admin"] == False