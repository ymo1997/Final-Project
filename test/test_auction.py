import pytest
from datetime import datetime
from time import sleep
from requests import post, get

server_url = 'http://localhost:5000'

def pytest_namespace():
    return {
        'newly_created_item_id': None,
        'newly_created_user_id': None,
        'newly_created_seller_id': None,
        'newly_created_overbidder_id': None,
        }

def test_data_preparation():
    params = {
        'email': 'lily@mail.com', 
        'password': 'JOHNSON',
        'first_name': 'Boris',
        'last_name':'Johnson',
    }
    api_url = server_url + '/user/create-account'

    response = post(api_url, json = params)
    pytest.newly_created_overbidder_id = response.json()["_id"]
    assert response.status_code == 200

    params = {
        'email': 'zhangyueyang7@gmail.com', 
        'password': 'JOHNSON',
        'first_name': 'Boris',
        'last_name':'Johnson',
    }
    api_url = server_url + '/user/create-account'

    response = post(api_url, json = params)
    pytest.newly_created_seller_id = response.json()["_id"]
    assert response.status_code == 200

    params = {
        'email': 'zyy1996zyy@hotmail.com', 
        'password': 'JOHNSON',
        'first_name': 'Boris',
        'last_name':'Johnson',
    }
    api_url = server_url + '/user/create-account'

    response = post(api_url, json = params)
    pytest.newly_created_user_id = response.json()["_id"]
    assert response.status_code == 200

    params = {
        'description': 'This pair of Chinese republic period miniature porcelain vases',
        'item_name': 'Pair Chinese Republic', 
        'seller_id': pytest.newly_created_seller_id, 
        'starting_price': 500.0, 
        'auction_start_time': datetime.now().timestamp(), 
        'auction_end_time': datetime.now().timestamp() + 2, 
        'category_id': 9,
        'condition': 2,
        'image_url': "https://www.flaticon.com/svg/static/icons/svg/914/914832.svg",
        'shipping_cost': 7.99
        }

    api_url = server_url + '/item/create-item'
    response = post(api_url, json = params)
    pytest.newly_created_item_id = response.json()["item_id"]
    assert response.status_code == 200


def test_bid_item():
    params = {
        'item_id' : pytest.newly_created_item_id,
    }
    api_url = server_url + '/item/get-item-info'
    response = post(api_url, json = params)
    record = response.json()
    current_auction_price = record["starting_price"]

    params = {
        'auction_user_id' : pytest.newly_created_user_id,
        'item_id' : pytest.newly_created_item_id,
        'auction_price' : current_auction_price + 100,
    }
    api_url = server_url + '/auction/bid-item'
    response = post(api_url, json = params)
    auction_id = response.json()["auction_id"]
    assert response.status_code == 200

    params['auction_price'] = current_auction_price + 100
    api_url = server_url + '/auction/bid-item'
    response = post(api_url, json = params)
    auction_id = response.json()["auction_id"]
    assert response.status_code == 400

    params['auction_price'] = current_auction_price + 400
    params['auction_user_id'] = pytest.newly_created_overbidder_id
    api_url = server_url + '/auction/bid-item'
    response = post(api_url, json = params)
    auction_id = response.json()["auction_id"]
    assert response.status_code == 200


def test_get_auction_history():
    params = {
        'item_id' : pytest.newly_created_item_id,
    }
    api_url = server_url + '/auction/get-auction-history'
    response = get(api_url, params = params)
    auction_list = response.json()['auction_list']
    assert len(auction_list) == 3


def test_list_user_shopping_cart_items():
    sleep(2)
    params = {
        'user_id': pytest.newly_created_overbidder_id
    }
    api_url = server_url + '/shopping-cart/list-user-shopping-cart-items'
    response = get(api_url, params = params)
    assert response.status_code == 200
    item_list = response.json()['item_list']
    assert len(item_list) == 1


def test_data_delete():
    params = {
        'account_id': pytest.newly_created_user_id
    }
    api_url = server_url + '/user/delete-account'
    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'account_id': pytest.newly_created_seller_id
    }
    api_url = server_url + '/user/delete-account'
    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'account_id': pytest.newly_created_overbidder_id
    }
    api_url = server_url + '/user/delete-account'
    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'item_id': pytest.newly_created_item_id
    }
    print(params)
    api_url = server_url + '/item/delete-item'
    response = post(api_url, json = params)
    assert response.status_code == 200



    



