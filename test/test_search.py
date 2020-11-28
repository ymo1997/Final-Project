import pytest
from datetime import datetime
from requests import post, get

server_url = 'http://localhost:5000'


def test_search_search_item_by_keyword():
    params = {
        'keyword': 'bi'
    }

    api_url = server_url + '/search/search-item-by-keyword'
    response = get(api_url, params = params)
    record = response.json()
    
    print(record["item_list"])
    assert response.status_code == 200
    assert len(record["item_list"]) == 3

    params = {
        'keyword': None
    }

    api_url = server_url + '/search/search-item-by-keyword'
    response = get(api_url, params = params)
    record = response.json()
    
    assert response.status_code == 200
    assert len(record["item_list"]) == 4


def test_search_search_item_by_category():
    params = {
        'category_id': 2
    }

    api_url = server_url + '/search/search-item-by-category'
    response = get(api_url, params = params)
    record = response.json()
    
    assert response.status_code == 200
    assert len(record["item_list"]) == 1

    params = {
        'category_id': 7
    }

    api_url = server_url + '/search/search-item-by-category'
    response = get(api_url, params = params)
    record = response.json()
    
    assert response.status_code == 200
    assert len(record["item_list"]) == 0


