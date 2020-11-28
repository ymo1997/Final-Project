import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'

# def test_bid_item():
#     params = {
#         'item_id' : 3,
#     }
    
#     api_url = server_url + '/item/get-item-info'
#     response = post(api_url, json = params)
#     record = response.json()
#     current_auction_price = record["current_auction_price"]

#     params = {
#         'auction_user_id' : 5,
#         'item_id' : 3,
#         'auction_price' : current_auction_price + 100,
#     }

#     api_url = server_url + '/auction/bid-item'
#     response = post(api_url, json = params)
#     auction_id = response.json()["auction_id"]
#     assert response.status_code == 200

#     params['auction_price'] = current_auction_price + 100

#     api_url = server_url + '/auction/bid-item'
#     response = post(api_url, json = params)
#     auction_id = response.json()["auction_id"]
#     assert response.status_code == 400

#     params = {
#         'item_id' : 3,
#     }
    
#     api_url = server_url + '/item/get-item-info'
#     response = post(api_url, json = params)
#     record = response.json()
#     current_auction_price = record["current_auction_price"]
#     if current_auction_price is None:
#         current_auction_price = record["starting_price"]

#     params = {
#         'auction_user_id' : 5,
#         'item_id' : 4,
#         'auction_price' : current_auction_price + 100,
#     }

#     api_url = server_url + '/auction/bid-item'
#     response = post(api_url, json = params)
#     auction_id = response.json()["auction_id"]
#     assert response.status_code == 200

#     params['auction_price'] = current_auction_price + 200

#     api_url = server_url + '/auction/bid-item'
#     response = post(api_url, json = params)
#     auction_id = response.json()["auction_id"]
#     assert response.status_code == 200


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






