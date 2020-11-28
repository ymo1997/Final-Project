import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'

def pytest_namespace():
    return {
        'newly_created_item_id': None,
        }


def test_bid_item():
    params = {
        'description': 'This pair of Chinese republic period miniature porcelain vases',
        'item_name': 'Pair Chinese Republic', 
        'seller_id': 2, 
        'starting_price': 500.0, 
        'auction_start_time': 1606432462, 
        'auction_end_time': 1606583144, 
        'category_id': 9,
        'condition': 2,
        'image_url': "https://www.flaticon.com/svg/static/icons/svg/914/914832.svg",
        'shipping_cost': 7.99
        }

    api_url = server_url + '/item/create-item'

    response = post(api_url, json = params)
    newly_created_item_id = response.json()["item_id"]
    assert response.status_code == 200

    params = {
        'email': 'Johnson@mail.com', 
        'password': 'JOHNSON',
        'first_name': 'Boris',
        'last_name':'Johnson',
    }
    api_url = server_url + '/user/create-account'

    response = post(api_url, json = params)
    newly_created_user_id = response.json()["_id"]
    assert response.status_code == 200

    params = {
        'item_id' : newly_created_item_id,
    }
    
    api_url = server_url + '/item/get-item-info'
    response = post(api_url, json = params)
    record = response.json()
    current_auction_price = record["starting_price"]

    params = {
        'auction_user_id' : newly_created_user_id,
        'item_id' : newly_created_item_id,
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

    params = {
        'item_id': pytest.newly_created_item_id
    }

    api_url = server_url + '/item/delete-item'
    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'account_id': pytest.newly_created_user_id
    }
    api_url = server_url + '/user/delete-account'

    response = post(api_url, json = params)
    assert response.status_code == 200




def test_get_auction_history():
    params = {
        'item_id' : 3,
    }
    api_url = server_url + '/auction/get-auction-history'
    response = get(api_url, params = params)
    auction_list = response.json()['auction_list']
    assert len(auction_list) == 3



# def test_list_item():
#     test_status = "ready"
#     result, data = auction_rpc.list_item(test_status)
#     assert result == True
#     assert len(data) > 0
#     result, data = auction_rpc.list_item("")
#     assert result == True
#     assert len(data) == 0


# def test_update_auction_status():
#     item_id = 111
#     result, status = auction_rpc.update_auction_status(item_id)
#     assert result == True
#     assert status == "completed"
#     # change status back
#     auction_rpc.change_auction_status(item_id, "ready")


# def test_set_auction_window():
#     item_id = 111
#     result, status = auction_rpc.set_auction_window(item_id, 888, 999)
#     assert result == True
#     result, status = auction_rpc.set_auction_window(item_id, 123, 456)
#     assert result == True






