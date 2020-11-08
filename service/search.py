from nameko.rpc import rpc, RpcProxy
from pymongo import MongoClient

class Search(object):
	name = "search"

	@rpc
	def search_user(self, keyword):
		return [], True, ""