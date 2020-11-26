import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'

def test_item_create_item():
    params = {
        'item_name': 'Pair Chinese Republic Period Miniature Vase Flower Bird', 
        'seller_id': 5, 
        'category_name': 'Asian Antiques', 
        'description': 'Up for sale from a recent estate in Honolulu Hawaii, this pair of Chinese republic period miniature porcelain vases with flower and bird motifs painted in famille rose enamels that show a red seal on their base. ', 
        'auction_start_time': datetime(2020, 12, 1, 10, 20, 0).timestamp(), 
        'auction_end_time': datetime(2020, 12, 10, 10, 20, 0).timestamp(), 
        'starting_price': '75'
    }
    api_url = server_url + '/item/create-item'

    response = post(api_url, json = params)
    assert response.status_code == 200







