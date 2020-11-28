import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'


def test_create_user_shopping_cart():
    params = {
        'user_id': 8000
    }
    api_url = server_url + '/shopping-cart/create-user-shopping-cart'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_add_item_to_user_shopping_cart():
    params = {
        'user_id': 8000,
        'item_id': 10000
    }
    api_url = server_url + '/shopping-cart/add-item-to-user-shopping-cart'

    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'user_id': 8000,
        'item_id': 10001
    }
    api_url = server_url + '/shopping-cart/add-item-to-user-shopping-cart'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_list_user_shopping_cart_items():
    params = {
        'user_id': 8000
    }
    api_url = server_url + '/shopping-cart/list-user-shopping-cart-items'
    response = get(api_url, params = params)
    assert response.status_code == 200
    
    item_list = response.json()['item_list']
    print(response.json())
    assert len(item_list) == 2
    
    params = {
        'user_id': 2
    }
    api_url = server_url + '/shopping-cart/list-user-shopping-cart-items'
    response = get(api_url, params = params)
    assert response.status_code == 200

    item_list = response.json()['item_list']
    print(item_list)
    assert len(item_list) == 1


def test_delete_item_from_user_shopping_cart():
    params = {
        'user_id' : 8000,
        'item_id': 10000
    }
    api_url = server_url + '/shopping-cart/delete-item-from-user-shopping-cart'

    response = post(api_url, json = params)
    assert response.status_code == 200

    
def test_delete_user_shopping_cart():
    params = {
        'user_id': 8000
    }
    api_url = server_url + '/shopping-cart/delete-user-shopping-cart'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_checkout_shopping_cart():
    params = {
        'user_id': 2
    }
    api_url = server_url + '/shopping-cart/checkout-shopping-cart'
    response = get(api_url, params = params)
    assert response.status_code == 200

    item_list = response.json()['item_list']
    assert len(item_list) == 1
    assert item_list[0]['price'] == 3500
    
    params = {
        'user_id': 2,
        'item_id': 2
    }
    api_url = server_url + '/shopping-cart/add-item-to-user-shopping-cart'
    response = post(api_url, json = params)
    assert response.status_code == 200

    

    




