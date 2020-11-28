from config import *

class Search(object):
    name = SEARCH

    item_rpc = RpcProxy(ITEM)


    @rpc
    def search_item_by_keyword(self, keyword):
        return self.item_rpc.list_items_by_keyword_on_item_name(keyword)


    @rpc
    def search_item_by_category(self, category_id):
        return self.item_rpc.list_items_by_category(category_id)