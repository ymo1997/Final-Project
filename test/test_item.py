import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'

def pytest_namespace():
    return {
        'newly_created_item_id': None,
        'newly_created_on_going_item_id': None,
        'newly_created_category_id': None
        }


def test_item_create_item():
    params = {
        'description': 'This pair of Chinese republic period miniature porcelain vases',
        'item_name': 'Pair Chinese Republic', 
        'seller_id': 2, 
        'starting_price': 500.0, 
        'auction_start_time': 1606432462, 
        'auction_end_time': 1606583144, 
        'category_id': 9
        }

    api_url = server_url + '/item/create-item'

    response = post(api_url, json = params)
    pytest.newly_created_item_id = response.json()["item_id"]
    assert response.status_code == 200

    params = {
        'description': 'Porcelain vases',
        'item_name': 'Pair England Republic', 
        'seller_id': 2, 
        'starting_price': 500.0, 
        'auction_start_time': 1606511730, 
        'auction_end_time': 1626583144, 
        'category_id': 9
        }

    api_url = server_url + '/item/create-item'

    response = post(api_url, json = params)
    pytest.newly_created_on_going_item_id = response.json()["item_id"]
    assert response.status_code == 200


def test_item_create_category():
    params = {
        'category_name' : 'Currency'
    }
    api_url = server_url + '/item/create-category'

    response = post(api_url, json = params)
    pytest.newly_created_category_id = response.json()["category_id"]
    assert response.status_code == 200


def test_item_update_item_info():
    params = {
        'item_id': pytest.newly_created_item_id,
        'item_name': 'Pair Chinese Republic Period Miniature Vase',
        'category_id': pytest.newly_created_category_id, 
        'description': 'This pair of Chinese republic period miniature porcelain vases with flower and bird motifs painted in famille rose enamels that show a red seal on their base. ', 
        'auction_start_time': datetime(2020, 12, 3, 10, 20, 0).timestamp(), 
        'auction_end_time': datetime(2020, 12, 12, 10, 20, 0).timestamp(), 
        'starting_price': 750
    }

    api_url = server_url + '/item/update-item-info'
    response = post(api_url, json = params)
    assert response.status_code == 200


def test_item_modify_category():
    params = {
        'category_id' : pytest.newly_created_category_id,
        'category_name' : 'Art Deco'
    }
    api_url = server_url + '/item/modify-category'

    response = post(api_url, json = params)
    assert response.status_code == 200


def test_item_list_category():
    api_url = server_url + '/item/list-category'

    response = get(api_url)
    assert response.status_code == 200
    assert response.json()['category_list'][-1]['category_name'] == 'Art Deco'


def test_item_get_item_info():
    params = {
        'item_id': pytest.newly_created_item_id
    }

    api_url = server_url + '/item/get-item-info'
    response = post(api_url, json = params)
    record = response.json()
    assert record["item_name"] == 'Pair Chinese Republic Period Miniature Vase'
    assert record["category_id"] == pytest.newly_created_category_id
    assert record["description"] == 'This pair of Chinese republic period miniature porcelain vases with flower and bird motifs painted in famille rose enamels that show a red seal on their base. '
    assert record["auction_start_time"] == datetime(2020, 12, 3, 10, 20, 0).timestamp()
    assert record["auction_end_time"] == datetime(2020, 12, 12, 10, 20, 0).timestamp()
    assert record["starting_price"] == 750


def test_item_report_item():
    params = {
        'item_id': pytest.newly_created_item_id
    }

    api_url = server_url + '/item/report-item'
    response = post(api_url, json = params)
    assert response.status_code == 200


def test_item_stop_item_auction():
    params = {
        'item_id': pytest.newly_created_on_going_item_id
    }

    api_url = server_url + '/item/stop-item-auction'
    response = get(api_url, params = params)
    assert response.status_code == 200


def test_item_delete_item():
    params = {
        'item_id': pytest.newly_created_item_id
    }

    api_url = server_url + '/item/delete-item'
    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'item_id': 3
    }

    api_url = server_url + '/item/delete-item'
    response = post(api_url, json = params)
    assert response.status_code == 400

    params = {
        'item_id': pytest.newly_created_on_going_item_id
    }

    api_url = server_url + '/item/delete-item'
    response = post(api_url, json = params)
    assert response.status_code == 200


def test_item_delete_category():
    params = {
        'category_id' : pytest.newly_created_category_id
    }
    api_url = server_url + '/item/delete-category'

    response = get(api_url, params = params)
    assert response.status_code == 200


def test_item_list_user_auctioning():
    params = {
        'auction_user_id': 4
    }

    api_url = server_url + '/item/list-user-auctioning'
    response = post(api_url, json = params)
    record = response.json()
    
    assert response.status_code == 200
    assert record["auction_list"][0]["auction_id"] == 1
    assert record["auction_list"][1]["auction_id"] == 2

def test_item_list_user_auctioning():
    params = {
        'status': "ready"
    }

    api_url = server_url + '/item/list-items'
    response = post(api_url, json = params)
    record = response.json()
    
    assert response.status_code == 200
    assert len(record["item_list"]) == 1

    params = {
        'status': "on-going"
    }

    api_url = server_url + '/item/list-items'
    response = post(api_url, json = params)
    record = response.json()
    
    assert response.status_code == 200
    assert len(record["item_list"]) == 1

    params = {
        'status': "completed"
    }

    api_url = server_url + '/item/list-items'
    response = post(api_url, json = params)
    record = response.json()
    
    assert response.status_code == 200
    assert len(record["item_list"]) == 1

    params = {
    }

    api_url = server_url + '/item/list-items'
    response = post(api_url, json = params)
    record = response.json()
    
    assert response.status_code == 200
    assert len(record["item_list"]) == 3
    print(record["item_list"])

    params = {
        'status': "reported"
    }

    api_url = server_url + '/item/list-items'
    response = post(api_url, json = params)
    record = response.json()
    
    assert response.status_code == 200
    assert len(record["item_list"]) == 0








