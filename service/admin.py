from nameko.rpc import rpc, RpcProxy

class Admin(object):
	name = "admin"
	user_rpc = RpcProxy("user")
	search_rpc = RpcProxy("search")

	@rpc
	def login(self, admin, password):
		if admin in database:
			if database[admin] == password:
				return True, "Suceeded: Admin {} logged in.".format(admin)
			else:
				return False, "Failed: Wrong password."
		else:
			return False, "Failed: Invalid Admin."

	@rpc
	def logout(self, admin):
		return True, "Suceeded: Logout Successfully"

	@rpc
	def suspend_user(self, username):
		return self.user_rpc.suspend_user(username)

	@rpc
	def create_user(self, username, password):
		return self.user_rpc.register(username, password)

	@rpc
	def delete_user(self, username):
		return self.user_rpc.delete_user(username, "", True)

	@rpc
	def edit_user_info(self, username, sex, age):
		return self.user_rpc.edit_user_info(username, sex, age)

	@rpc
	def search_user(self, keyword):
		return self.search_rpc.search_user(keyword)

