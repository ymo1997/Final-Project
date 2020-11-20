import pytest
import sys
sys.path.append("..")
from service.bidding import Bidding

bidding_rpc = Bidding()

def test_user_register():
    test_status = "bidding"
    result, data = bidding_rpc.list_item(test_status)
    assert result == True
    assert len(data) > 0
    result, data = bidding_rpc.list_item("")
    assert result == True
    assert len(data) == 0