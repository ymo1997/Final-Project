from config import *

#---------- CONFIG ----------#
cursor = getDatabaseCusor(AUCTION)


#---------- DATA MODEL ----------#
AUCTION_ID = "auction_id"
AUCTION_USER_ID = "auction_user_id"
ITEM_ID = "item_id"
AUCTION_PRICE = "auction_price"
AUCTION_TIME = "auction_time"
STATUS = "status"

STATUS_VALID = "valid"
STATUS_INVALID = "invalid"

MESSAGE = "msg"
AUCTION_LIST = "auction_list"


class Auction(object):
    name = AUCTION

    item_rpc = RpcProxy(ITEM)

    @rpc
    def bid_item(self, auction_user_id, item_id, auction_price):
        self.item_rpc.update_all_auctions_status()
        returned_data = {AUCTION_ID: None, MESSAGE: None}
        auction_time = datetime.now().timestamp()

        params = (auction_user_id, item_id, auction_price, auction_time, STATUS_INVALID)
        query = """INSERT INTO auction (auction_user_id, item_id, \
            auction_price, auction_time, status) \
            VALUES (%d, %d, %f, %d, '%s') RETURNING auction_user_id;""" % params
        try:
            cursor.execute(query)
            auction_id = cursor.fetchone()[0]
            returned_data[AUCTION_ID] = auction_id
        except Exception as e:
            log_for_except(__name__, e)
            returned_data[MESSAGE] = auction_bid_item_failed
            return False, returned_data
        result, msg = self.item_rpc.update_item_with_bid(auction_id, auction_user_id, item_id, auction_price, auction_time)

        if result:
            returned_data[MESSAGE] = auction_bid_item_suceeded
            params = (STATUS_VALID, auction_id)
            query = """UPDATE auction SET status = '%s' WHERE auction_id = %d""" % params
            cursor.execute(query)
            return True, returned_data
        else:
            returned_data[MESSAGE] = auction_bid_item_failed
            return False, returned_data
        

    @rpc
    def get_auction_history(self, item_id):
        self.item_rpc.update_all_auctions_status()
        returned_data = {MESSAGE: None, AUCTION_LIST: None}
        query = "SELECT * FROM auction WHERE item_id = %s " %(item_id)

        if try_execute_sql(cursor, query, __name__):
            returned_data[MESSAGE] = auction_get_auction_history_suceeded
            data = cursor.fetchall()
            auction_list = []
            for auction_histroy in data:
                auction_list.append({
                    AUCTION_ID: auction_histroy[0],
                    AUCTION_USER_ID: auction_histroy[1],
                    ITEM_ID: auction_histroy[2],
                    AUCTION_PRICE: auction_histroy[3],
                    AUCTION_TIME: auction_histroy[4],
                    STATUS: auction_histroy[5]})

            returned_data[AUCTION_LIST] = auction_list

            return True, returned_data
        else:
            returned_data[MESSAGE] = auction_get_auction_history_failed
            return False, returned_data
        res = cursor.fetchall() 
        return True, res








#     @rpc
#     def list_item(self, status):
#         query = "SELECT * FROM item_table WHERE status = '%s'" %(status)
#         item_db_cursor.execute(query)
#         res = item_db_cursor.fetchall() 
#         return True, res

#     @rpc
#     def update_auction_status(self, item_id):
#         # we have three status 'ready', 'auction', 'completed'
#         query = "SELECT auction_start_time, auction_end_time, status FROM item_table WHERE item_id = %s" %(item_id)
#         item_db_cursor.execute(query)
#         res = item_db_cursor.fetchone()

#         auction_start_time = int(res[0])
#         auction_end_time = int(res[1])
#         status = str(res[2])

#         current_time = time.time()
#         new_status = None

#         if current_time < auction_start_time:
#             if status == "ready":
#                 return False, "ready"
#             else:
#                 new_status = "ready"
#         elif auction_start_time <= current_time <= auction_end_time:
#             if status == "auction":
#                 return False, "auction"
#             else:
#                 new_status = "auction"
#         else:
#             if status == "completed":
#                 return False, "completed"
#             else:
#                 new_status = "completed"

#         if new_status:
#             query = "UPDATE item_table SET status = '%s' WHERE item_id = '%s'" %(new_status, item_id)
#             item_db_cursor.execute(query)
#             return True, new_status

#     @rpc
#     def set_auction_window(self, item_id, start_time, end_time):
#         if end_time <= start_time:
#             return False, "Failed: End time must be larger than start time."
        
#         query = "UPDATE item_table SET auction_start_time = '%s', auction_end_time = '%s'\
#                  WHERE item_id = '%s'" %(start_time, end_time, item_id)
#         item_db_cursor.execute(query)
#         return True, "Succeeded"

    


#     @rpc
#     def add_to_cart(self, item_id, user_id, cart_id):
#         query = "INSERT INTO shopping_cart_table VALUES(%s,%s, %s)" % (cart_id, item_id, user_id)
#         item_db_cursor.execute(query)
#         return True, "Succeeded"






#     ####### for testing/admin ######'
#     @rpc
#     def change_bidding_price(self, item_id, user_id, new_price):
#         query = "UPDATE item_table SET current_auction_price = %s, current_auction_buyer_id = %s\
#                  WHERE item_id = '%s'" %(new_price, user_id, item_id)
#         item_db_cursor.execute(query)
#         return True, "Succeeded"



#     @rpc
#     def change_auction_status(self, item_id, new_status):
#         # Used for testing/admin, change auction status without checking anything
#         query = "UPDATE item_table SET status = '%s' WHERE item_id = '%s'" %(new_status, item_id)
#         item_db_cursor.execute(query)
#         return True, new_status
# # params = (ITEM_STATUS_READY, now_timestamp)
# #         query = "UPDATE item SET status = '%s' WHERE %d < auction_start_time" % params
# #         try:
# #             cursor.execute(query)
# #         except Exception as e:
# #             log_for_except(__name__, e)
# #             return



# #         params = (ITEM_STATUS_COMPLETED, now_timestamp)
# #         query = "UPDATE item SET status = '%s' WHERE %d > auction_end_time" % params
# #         try:
# #             cursor.execute(query)
# #         except Exception as e:
# #             log_for_except(__name__, e)
# #             return





