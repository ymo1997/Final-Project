import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'


def test_create_user_shopping_cart():
    params = {
        'user_id' : 10000
    }
    api_url = server_url + '/shopping-cart/create-user-shopping-cart'

    response = post(api_url, json = params)
    assert response.status_code == 200
