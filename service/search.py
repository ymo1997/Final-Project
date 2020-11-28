from nameko.rpc import rpc, RpcProxy
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime
from responses import *


class Search(object):
    name = "search"

    item_rpc = RpcProxy("item")


    @rpc
    def search_item_by_keyword(self, keyword):
        return self.item_rpc.list_items_by_keyword_on_item_name(keyword)


    @rpc
    def search_item_by_category(self, category_id):
        return self.item_rpc.list_items_by_category(category_id)