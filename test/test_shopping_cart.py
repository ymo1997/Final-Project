import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'


def test_create_user_shopping_cart():
    params = {
        'user_id': 10000
    }
    api_url = server_url + '/shopping-cart/create-user-shopping-cart'

    response = post(api_url, json = params)
    assert response.status_code == 200


# def test_add_item_to_user_shopping_cart():
#     params = {
#         'user_id': 10000,
#         'item_id': 10000
#     }
#     api_url = server_url + '/shopping-cart/add-item-to-user-shopping-cart'

#     response = post(api_url, json = params)
#     assert response.status_code == 200


# def test_delete_item_from_user_shopping_cart():
#     params = {
#         'user_id' : 10000,
#         'item_id': 10000
#     }
#     api_url = server_url + '/shopping-cart/delete-item-from-user-shopping-cart'

#     response = post(api_url, json = params)
#     assert response.status_code == 200

    
# def test_delete_user_shopping_cart():
#     params = {
#         'user_id': 10000
#     }
#     api_url = server_url + '/shopping-cart/delete-user-shopping-cart'

#     response = post(api_url, json = params)
#     assert response.status_code == 200
