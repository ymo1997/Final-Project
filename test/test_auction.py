import pytest
import sys
sys.path.append("..")
from service.auction import Auction

auction_rpc = Auction()

def test_list_item():
    test_status = "ready"
    result, data = auction_rpc.list_item(test_status)
    assert result == True
    assert len(data) > 0
    result, data = auction_rpc.list_item("")
    assert result == True
    assert len(data) == 0


def test_update_auction_status():
    item_id = 111
    result, status = auction_rpc.update_auction_status(item_id)
    assert result == True
    assert status == "completed"
    # change status back
    auction_rpc.change_auction_status(item_id, "ready")



def test_set_auction_window():
    item_id = 111
    result, status = auction_rpc.set_auction_window(item_id, 888, 999)
    assert result == True
    result, status = auction_rpc.set_auction_window(item_id, 123, 456)
    assert result == True


def test_increment_bidding_price():
    item_id = 111
    result, msg = auction_rpc.increment_bidding_price(item_id, 333, 1)
    assert result == False
    result, msg = auction_rpc.increment_bidding_price(item_id, 333, 200)
    assert result == True
    # change data back
    auction_rpc.change_bidding_price(item_id, 'NULL', 20)



