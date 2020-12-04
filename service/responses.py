import logging
def try_execute_sql(cursor, query, filename):
    try:
        print(query)
        cursor.execute(query)
    except Exception as e:
        print(e)
        log_for_except(filename, e)
        return False
    return True

def log_for_except(filename, e):
	logging.error("Exception in %s: %s" % (filename, e))

#---------- RESPONSE ----------#
MESSAGE = "msg"

#---------- USER -----------#
user_create_account_suceeded = "Suceeded: Account is created."
user_create_account_failed = "Failed: Account is existed."

user_update_account_info_suceeded = "Suceeded: Account info is changed."
user_update_account_info_failed = "Failed: Account info is not changed."

user_delete_account_suceeded = "Suceeded: Account is deleted."
user_delete_account_failed_db = "Failed: Account is not deleted in db."
user_delete_account_failed_not_existed = "Failed: Account is not existed."

user_suspend_account_suceeded = "Suceeded: Account is suspended."
user_suspend_account_failed = "Failed: Account is not suspended."

user_get_account_info_suceeded = "Suceeded: Account info is retrieved."
user_get_account_info_failed = "Failed: Account info is not retrieved."

user_verify_login_input_suceeded = "Suceeded: Username and password match."
user_verify_login_input_failed_invalid_username = "Failed: Invalid username."
user_verify_login_input_failed_wrong_password = "Failed: Wrong password."


#---------- ADMIN -----------#
admin_create_account_suceeded = "Suceeded: Account is created."
admin_create_account_failed = "Failed: Account is existed."

admin_get_account_info_suceeded = "Suceeded: Account info is retrieved."
admin_get_account_info_failed = "Failed: Account info is not retrieved."

admin_delete_admin_account_suceeded = "Suceeded: Account is deleted."
admin_delete_admin_account_failed_db = "Failed: Account is not deleted in db."
admin_delete_admin_account_failed_not_existed = "Failed: Account is not existed."

admin_verify_login_input_suceeded = "Suceeded: Admin and password match."
admin_verify_login_input_failed_invalid_admin = "Failed: Invalid admin."
admin_verify_login_input_failed_wrong_password = "Failed: Wrong password."


#---------- ITEM ----------#
item_create_item_failed = "Failed: Item is not created."
item_create_item_suceeded = "Suceeded: Item is created."

item_delete_item_failed = "Failed: Item is not deleted."
item_delete_item_suceeded = "Suceeded: Item is deleted."

item_update_item_info_failed = "Failed: Item info is not updated."
item_update_item_info_suceeded = "Suceeded: Item info is updated."

item_get_item_info_failed = "Failed: Item info is not retrieved."
item_get_item_info_suceeded = "Suceeded: Item info is retrieved."

item_report_item_failed = "Failed: Item info is not reported."
item_report_item_suceeded = "Suceeded: Item info is reported."

item_create_category_failed = "Failed: category is not created."
item_create_category_suceeded = "Suceeded: category is created."

item_update_category_failed = "Failed: category is not updated."
item_update_category_suceeded = "Suceeded: category is updated."

item_delete_category_failed = "Failed: category is not deleted."
item_delete_category_suceeded = "Suceeded: category is deleted."

item_list_categories_failed = "Failed: category list is not retrieved."
item_list_categories_suceeded = "Suceeded: category list is not retrieved."

item_update_item_with_bid_failed_db = "Failed: Item auction info is not updated due to database query."
item_update_item_with_bid_failed_status = "Failed: Item auction info is not updated due to item status."
item_update_item_with_bid_failed_price = "Failed: Item auction info is not updated due to low price."
item_update_item_with_bid_suceeded = "Suceeded: Item auction info is updated."

item_list_user_auctioning_failed = "Failed: User's auctioning info is not retrieved."
item_list_user_auctioning_suceeded = "Suceeded: User's auctioning info is retrieved."

item_list_item_failed = "Failed: list is not retrieved."
item_list_item_suceeded = "Suceeded: list info is retrieved."

item_stop_item_auction_failed = "Failed: Item auction is not stopped."
item_stop_item_auction_suceeded = "Suceeded: Item auction is stopped."

item_list_item_by_keyword_failed = "Failed: item searching result is not retrieved."
item_items_by_keyword_suceeded = "Suceeded: item searching result info is retrieved."

item_list_item_by_category_failed = "Failed: item searching result is not retrieved."
item_items_by_category_suceeded = "Suceeded: item searching result info is retrieved."

item_list_user_sell_item_failed = "Failed: user's items result is not retrieved."
item_list_user_sell_item_suceeded = "Suceeded: user's items result info is retrieved."

item_delete_user_sell_item_failed = "Failed: user's items is not deleted."
item_delete_user_sell_item_suceeded = "Suceeded: user's items info is deleted."

#---------- AUCTION ----------#
auction_bid_item_failed = "Failed: Item is not bid."
auction_bid_item_suceeded = "Suceeded: Item is bid."

auction_get_auction_history_failed = "Failed: Auction history is not retrieved."
auction_get_auction_history_suceeded = "Suceeded: Auction history is retrieved."


#---------- SHOPPING_CART ----------#
shopping_cart_create_user_shopping_cart_failed = "Failed: User's shopping cart is not created."
shopping_cart_create_user_shopping_cart_suceeded = "Suceeded: User's shopping cart is created."

shopping_cart_delete_user_shopping_cart_failed = "Failed: User's shopping cart is not deleted."
shopping_cart_delete_user_shopping_cart_suceeded = "Suceeded: User's shopping cart is deleted."

shopping_cart_add_item_to_user_shopping_cart_failed = "Failed: Item is not added to user's shopping cart."
shopping_cart_add_item_to_user_shopping_cart_suceeded = "Suceeded: Item is added to user's shopping cart."

shopping_cart_delete_item_from_user_shopping_cart_failed = "Failed: Item is not deleted to user's shopping cart."
shopping_cart_delete_item_from_user_shopping_cart_suceeded = "Suceeded: Item is deleted to user's shopping cart."

shopping_cart_checkout_shopping_cart_failed = "Failed: Items in shopping cart is not checked out."
shopping_cart_checkout_shopping_cart_suceeded = "Suceeded: Items in shopping cart is checked out."

shopping_cart_list_user_shopping_cart_items_failed = "Failed: Items in shopping cart is not retrieved."
shopping_cart_list_user_shopping_cart_items_suceeded = "Suceeded: Items in shopping cart is retrieved."


#---------- LOGIN ----------#





#---------- SEARCH ----------#







