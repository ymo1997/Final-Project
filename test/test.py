import pytest
from requests import post, get

server_url = 'http://localhost:5000'

def pytest_namespace():
    return {
        'newly_created_user_id': None
        }

def test_user_create_account():
    params = {
        'email': 'aasdfaagfhfsafasd@mail.com', 
        'password': 'JOHNSON',
        'first_name': 'Boris',
        'last_name':'Johnson',
    }
    api_url = server_url + '/user/create-account'

    response = post(api_url, json = params)
    print("DEBUG")
    print(response.text)
    pytest.newly_created_user_id = response.json()["_id"]
    assert response.status_code == 200

    response = post(api_url, json = params)
    assert response.status_code == 400


def test_user_info_edit():
    params = {
        'account_id': pytest.newly_created_user_id, 
        'email': 'Johnson@mail.com', 
        'password': "JOHNSON", 
        'first_name': 'Jack', 
        'last_name': 'Biden',
    }
    api_url = server_url + '/user/update-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200

    params = {
        'account_id': pytest.newly_created_user_id
    }

    api_url = server_url + '/login/get-account-info'

    response = post(api_url, json = params)
    assert response.status_code == 200
    assert response.json()['email'] == 'Johnson@mail.com'
    assert response.json()['first_name'] == 'Jack'
    assert response.json()['last_name'] == 'Biden'


def test_user_delete():
    params = {
        'description': 'This pair of Chinese republic period miniature porcelain vases',
        'item_name': 'Pair Chinese Republic', 
        'seller_id': pytest.newly_created_user_id, 
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
        'account_id': pytest.newly_created_user_id
    }
    api_url = server_url + '/user/delete-account'

    response = post(api_url, json = params)
    assert response.status_code == 200
    
    response = post(api_url, json = params)
    assert response.status_code == 400

    params = {
        'item_id': newly_created_item_id
    }

    api_url = server_url + '/item/get-item-info'
    response = post(api_url, json = params)
    record = response.json()
    assert response.status_code == 400

