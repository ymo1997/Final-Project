from flask import Flask, request, jsonify
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy
from datetime import datetime

#---------- CONFIG ----------#
app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


#---------- USER APIs ----------#
@app.route('/user/create-account', methods=['POST'])
def user_create_account():
    """
    user-create-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: user-create-account
          properties:
            email:
              type: string
            first_name:
              type: string
            last_name:
              type: string
            password:
              type: string
    responses:
      200:
        description: Suceeded - User is created.
      400:
        description: Failed - User is existed.
      json:
        description: Keys - account_id
    """
    username = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    password = request.json.get('password')
    date_joined = datetime.today().strftime('%Y-%m-%d')
    with ClusterRpcProxy(CONFIG) as rpc:
          result, msg = rpc.user.create_account(username, password, first_name, last_name, date_joined)
    if result:
        return msg, 200
    return msg, 400


@app.route('/user/update-account-info', methods=['POST'])
def user_update_account_info():
    """
    user-update-account-info API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: user-update-account-info
          properties:
            account_id:
              type: integer
            email:
              type: string
            password:
              type: string
            first_name:
              type: string
            last_name:
              type: string
    responses:
      200:
        description: Suceeded - User info is changed.
      400:
        description: Failed - User info is not changed.
    """
    account_id = request.json.get('account_id')
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.update_account_info(account_id, email, password, first_name, last_name)
    if result:
        return msg, 200
    return msg, 400


@app.route('/user/delete-account', methods=['POST'])
def user_delete_account():
    """
    user-delete-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: user-delete-account
          properties:
            account_id:
              type: integer
    responses:
      200:
        description: Succeeded - user is deleted.
      400:
        description: Failed - user is not deleted.
    """
    account_id = request.json.get('account_id')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.delete_account(account_id = account_id)
    if result:
        return msg, 200
    return msg, 400


@app.route('/user/suspend-account', methods=['POST'])
def user_suspend_account():
    """
    user-suspend-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-suspend-user-account
          properties:
            account_id:
              type: string
    responses:
      200:
        description: Succeeded - user is suspended.
      400:
        description: Failed - user is not suspended.
    """
    account_id = request.json.get('account_id')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.suspend_account(account_id = account_id)
    if result:
        return msg, 200
    return msg, 400


#---------- ADMIN APIs ----------#
@app.route('/admin/create-user-account', methods=['POST'])
def admin_create_user_account():
    """
    admin-create-user-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-create-user-account
          properties:
            username:
              type: string
            password:
              type: string
            first_name:
              type: string
            last_name:
              type: string
    responses:
      200:
        description: Suceeded - User is created.
      400:
        description: Failed - User is existed.
      json:
        description: Keys - account_id
    """
    username = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    date_joined = datetime.today().strftime('%Y-%m-%d')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.create_user_account(username, password, first_name, last_name, date_joined)
    if result:
        return msg, 200
    return msg, 400


@app.route('/admin/delete-user-account', methods=['POST'])
def admin_delete_user_account():
    """
    admin-delete-user-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-delete-user-account
          properties:
            email:
              type: string
    responses:
      200:
        description: Succeeded - user is deleted.
      400:
        description: Failed - user is not deleted.
    """
    email = request.json.get('email')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.delete_user_account(email)
    if result:
        return msg, 200
    return msg, 400


@app.route('/admin/update-user-account-info', methods=['POST'])
def admin_update_user_account_info():
    """
    admin-update-user-account-info API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-update-user-account-info
          properties:
            account_id:
              type: integer
            email:
              type: string
            password:
              type: string
            first_name:
              type: string
            last_name:
              type: string
    responses:
      200:
        description: Succeeded - user info is changed.
      400:
        description: Failed - user info is not changed.
    """
    account_id = request.json.get('account_id')
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.update_user_account_info(account_id, email, password, first_name, last_name)
    if result:
        return msg, 200
    return msg, 400


@app.route('/admin/suspend-user-account', methods=['POST'])
def admin_suspend_user_account():
    """
    admin-suspend-user-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-suspend-user-account
          properties:
            email:
              type: string
    responses:
      200:
        description: Succeeded - user is suspended.
      400:
        description: Failed - user is not suspended.
    """
    username = request.json.get('email')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.suspend_user_account(username)
    if result:
        return msg, 200
    return msg, 400


@app.route('/admin/create-admin-account', methods=['POST'])
def admin_create_admin_account():
    """
    admin-create-admin-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-create-admin-account
          properties:
            email:
              type: string
            first_name:
              type: string
            last_name:
              type: string
            password:
              type: string
    responses:
      200:
        description: Suceeded - User is created.
      400:
        description: Failed - User is existed.
      json:
        description: Keys - account_id
    """
    username = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    password = request.json.get('password')
    date_joined = datetime.today().strftime('%Y-%m-%d')
    with ClusterRpcProxy(CONFIG) as rpc:
          result, msg = rpc.admin.create_admin_account(username, password, first_name, last_name, date_joined)
    if result:
        return msg, 200
    return msg, 400


@app.route('/admin/delete-admin-account', methods=['POST'])
def admin_delete_admin_account():
    """
    admin-delete-admin-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-delete-admin-account
          properties:
            email:
              type: string
    responses:
      200:
        description: Succeeded - account is deleted.
      400:
        description: Failed - account is not deleted.
    """
    email = request.json.get('email')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.delete_admin_account(email)
    if result:
        return msg, 200
    return msg, 400



#---------- ITEM APIs ----------#
@app.route('/item/create-item', methods=['POST'])
def item_create_item():
    """
    item-create-item API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_create_item
          properties:
            item_name:
              type: string
            seller_id:
              type: integer
            category_id:
              type: integer
            description:
              type: string
            auction_start_time:
              type: integer
            auction_end_time:
              type: integer
            starting_price:
              type: float
            condition:
              type: integer
            image_url:
              type: string
            shipping_cost:
              type: float
    responses:
      200:
        description: Succeeded - item is created.
      400:
        description: Failed - item is not created.
      data:
        description: Keys - item_id, msg
    """
    item_name = request.json.get('item_name')
    seller_id = request.json.get('seller_id')
    category_id = request.json.get('category_id')
    description = request.json.get('description')
    auction_start_time = request.json.get('auction_start_time')
    auction_end_time = request.json.get('auction_end_time')
    starting_price = request.json.get('starting_price')
    condition = request.json.get('condition')
    image_url = request.json.get('image_url')
    shipping_cost = request.json.get('shipping_cost')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.item.create_item(item_name, 
        seller_id, category_id, description, 
        auction_start_time, auction_end_time,
        starting_price, condition, image_url, shipping_cost)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/item/delete-item', methods=['POST'])
def item_delete_item():
    """
    item-delete-item API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item-delete-item
          properties:
            item_id:
              type: integer
    responses:
      200:
        description: Succeeded - item is deleted.
      400:
        description: Failed - item is not deleted.
    """
    item_id = request.json.get('item_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.item.delete_item(item_id)
    if result:
        return msg, 200
    return msg, 400


@app.route('/item/update-item-info', methods=['POST'])
def item_update_item_info():
    """
    item-update-item-info API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_update_item_info
          properties:
            item_id:
              type: integer
            item_name:
              type: string
            category_id:
              type: integer
            description:
              type: string
            auction_start_time:
              type: integer
            auction_end_time:
              type: integer
            starting_price:
              type: float
            condition:
              type: integer
            image_url:
              type: string
            shipping_cost:
              type: float
    responses:
      200:
        description: Succeeded - item info is updated.
      400:
        description: Failed - item info is not updated.
    """
    item_id = request.json.get('item_id')
    item_name = request.json.get('item_name')
    seller_id = request.json.get('seller_id')
    category_id = request.json.get('category_id')
    description = request.json.get('description')
    auction_start_time = request.json.get('auction_start_time')
    auction_end_time = request.json.get('auction_end_time')
    starting_price = request.json.get('starting_price')
    condition = request.json.get('condition')
    image_url = request.json.get('image_url')
    shipping_cost = request.json.get('shipping_cost')


    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.item.update_item_info(
        item_id, item_name, category_id, 
        description, auction_start_time, auction_end_time,
        starting_price, condition, image_url, shipping_cost)

    if result:
        return msg, 200
    return msg, 400


@app.route('/item/get-item-info', methods=['POST'])
def item_get_item_info():
    """
    item-get-item-info API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_get_item_info
          properties:
            item_id:
              type: integer
    responses:
      200:
        description: Succeeded - item is reported.
      400:
        description: Failed - item is not reported.
      data:
        description: Keys - item_id, item_name, seller_id, buyer_id, category_id, description, status, auction_start_time, auction_end_time, starting_price, current_auction_price, current_auction_buyer_id, msg
    """
    item_id = request.json.get('item_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.item.get_item_info(item_id)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/item/report-item', methods=['POST'])
def item_report_item():
    """
    item-report-item API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_report_item
          properties:
            item_id:
              type: integer
    responses:
      200:
        description: Succeeded - item is reported.
      400:
        description: Failed - item is not reported.
    """
    item_id = request.json.get('item_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.item.report_item(item_id)

    if result:
        return msg, 200
    return msg, 400


@app.route('/item/create-category', methods=['POST'])
def item_create_category():
    """
    item-create-category API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_create_category
          properties:
            category_name:
              type: string
    responses:
      200:
        description: Succeeded - category is created.
      400:
        description: Failed - category is not created.
      data:
        description: Keys - category_id, msg

    """
    category_name = request.json.get('category_name')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.item.create_category(category_name)
    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/item/delete-category', methods=['GET'])
def item_delete_category():
    """
    item-delete-category API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_delete_category
          properties:
            category_id:
              type: integer
    responses:
      200:
        description: Succeeded - category is deleted.
      400:
        description: Failed - category is not deleted.

    """
    category_id = int(request.args.get('category_id'))

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.item.delete_category(category_id)
    if result:
        return msg, 200
    return msg, 400


@app.route('/item/modify-category', methods=['POST'])
def item_modify_category():
    """
    item-modify-category API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_modify_category
          properties:
            category_id:
              type: integer
            category_name:
              type: string
    responses:
      200:
        description: Succeeded - category is modified.
      400:
        description: Failed - category is not modified.

    """
    category_id = request.json.get('category_id')
    category_name = request.json.get('category_name')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.item.modify_category(category_id, category_name)
    if result:
        return msg, 200
    return msg, 400


@app.route('/item/list-category', methods=['GET'])
def item_list_category():
    """
    item-list-category API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_list_category
          properties:
    responses:
      200:
        description: Succeeded - category list is retrieved.
      400:
        description: Failed - category is not retrieved.
    """

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.item.list_categories()
    if result:
        return data, 200
    return data, 400


@app.route('/item/list-user-auctioning', methods=['POST'])
def item_list_user_auctioning():
    """
    item-list-user-auctioning API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item_list_user_auctioning
          properties:
            auction_user_id:
              type: integer
    responses:
      200:
        description: Succeeded - User's auctioning info is retrieved.
      400:
        description: Failed - User's auctioning info is not retrieved.
      data:
        description: Keys - auction_list, msg
    """
    auction_user_id = request.json.get('auction_user_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.item.list_user_auctioning(auction_user_id)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/item/list-items', methods=['POST'])
def item_list_items():
    """
    item-list-items API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item-list-items
          properties:
            status:
              type: string (Optional, if input, choose from ready, on-going, completed, reported)
    responses:
      200:
        description: Succeeded - list is retrieved.
      400:
        description: Failed - list is not retrieved.
      data:
        description: Keys - item_list, msg
    """
    status = request.json.get('status')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.item.list_items(status)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/item/stop-item-auction', methods=['GET'])
def item_stop_item_auction():
    """
    item-stop-item-auction API 
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item-stop-item-auction
          properties:
            item_id:
              type: integer
    responses:
      200:
        description: Succeeded - item auction is stopped.
      400:
        description: Failed - item auction is not stopped.
    """
    item_id = request.args.get("item_id")
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.item.stop_item_auction(int(item_id))
    if result:
        return msg, 200
    return msg, 400


@app.route('/item/list-user-sell-items', methods=['POST'])
def item_list_user_sell_items():
    """
    item-list-user-sell-items API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: list-user-sell-items
          properties:
            user_id:
              type: integer
    responses:
      200:
        description: Succeeded - list is retrieved.
      400:
        description: Failed - list is not retrieved.
      data:
        description: Keys - item_list, msg
    """
    user_id = request.json.get('user_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.item.list_user_sell_items(user_id)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


#---------- AUCTION APIs ----------#
@app.route('/auction/bid-item', methods=['POST'])
def auction_bid_item():
    """
    auction-bid-item API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: auction-bid-item
          properties:
            auction_user_id:
              type: integer
            item_id:
              type: integer
            auction_price:
              type: float
    responses:
      200:
        description: Succeeded - item is bid.
      400:
        description: Failed - item is not bid.
      data:
        description: Keys - auction_id, msg

    """
    auction_user_id = request.json.get('auction_user_id')
    item_id = request.json.get('item_id')
    auction_price = request.json.get('auction_price')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.auction.bid_item(auction_user_id, item_id, auction_price)
    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/auction/get-auction-history', methods=['GET'])
def get_auction_history():
    """
    get-auction-history API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: get-auction-history
          properties:
            item_id:
              type: integer
    responses:
      200:
        description: Succeeded - auction history is retrieved.
      400:
        description: Failed - auction history is not retrieved
      data:
        description: Keys - data, msg

    """
    item_id = request.args.get('item_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.auction.get_auction_history(item_id)
    if result:
        return jsonify(data), 200
    return jsonify(data), 400


#---------- SHOPPING_CART APIs ----------#

@app.route('/shopping-cart/create-user-shopping-cart', methods=['POST'])
def shopping_cart_create_user_shopping_cart():
    """
    shopping-cart-create-user-shopping-cart API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: shopping-cart-create-user-shopping-cart
          properties:
            user_id:
              type: integer
    responses:
      200:
        description: Succeeded - User's shopping cart is created.
      400:
        description: Failed - User's shopping cart is not created.

    """
    user_id = request.json.get('user_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.shopping_cart.create_user_shopping_cart(user_id)
    if result:
        return msg, 200
    return msg, 400


@app.route('/shopping-cart/delete-user-shopping-cart', methods=['POST'])
def shopping_cart_delete_user_shopping_cart():
    """
    shopping-cart-delete-user-shopping-cart API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: shopping-cart-delete-user-shopping-cart
          properties:
            user_id:
              type: integer
    responses:
      200:
        description: Succeeded - User's shopping cart is deleted.
      400:
        description: Failed - User's shopping cart is not deleted.

    """
    user_id = request.json.get('user_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.shopping_cart.delete_user_shopping_cart(user_id)
    if result:
        return msg, 200
    return msg, 400


@app.route('/shopping-cart/add-item-to-user-shopping-cart', methods=['POST'])
def shopping_cart_add_item_to_user_shopping_cart():
    """
    shopping-cart-add-item-to-user-shopping-cart API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: shopping-cart-add-item-to-user-shopping-cart
          properties:
            user_id:
              type: integer
            item_id:
              type: integer
    responses:
      200:
        description: Succeeded - Item is added to user's cart.
      400:
        description: Failed - Item is not added to user's cart.

    """
    user_id = request.json.get('user_id')
    item_id = request.json.get('item_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.shopping_cart.add_item_to_user_shopping_cart(item_id, user_id)
    if result:
        return msg, 200
    return msg, 400


@app.route('/shopping-cart/delete-item-from-user-shopping-cart', methods=['POST'])
def shopping_cart_delete_item_from_user_shopping_cart():
    """
    shopping-cart-delete-item-from-user-shopping-cart API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: shopping-cart-add-item-to-user-shopping-cart
          properties:
            user_id:
              type: integer
            item_id:
              type: integer
    responses:
      200:
        description: Succeeded - Item is deleted from user's cart.
      400:
        description: Failed - Item is not deleted from user's cart.

    """
    user_id = request.json.get('user_id')
    item_id = request.json.get('item_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.shopping_cart.delete_item_from_user_shopping_cart(item_id, user_id)
    if result:
        return msg, 200
    return msg, 400


@app.route('/shopping-cart/checkout-shopping-cart', methods=['GET'])
def shopping_cart_checkout_shopping_cart():
    """
    checkout-shopping-cart API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: checkout-shopping-cart
          properties:
            user_id:
              type: integer
    responses:
      200:
        description: Succeeded - items are checked out.
      400:
        description: Failed - items are not checked out.
      data:
        description: Keys - item_list, msg
    """
    user_id = request.args.get('user_id')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.shopping_cart.checkout_shopping_cart(user_id)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/shopping-cart/list-user-shopping-cart-items', methods=['GET'])
def shopping_cart_list_user_shopping_cart_items():
    """
    list-user-shopping-cart-items API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: checkout-shopping-cart
          properties:
            user_id:
              type: integer
    responses:
      200:
        description: Succeeded - user's shopping cart item list is retrieved.
      400:
        description: Failed - user's shopping cart item list is retrieved.
      data:
        description: Keys - item_list, msg
    """
    user_id = int(request.args.get('user_id'))

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.shopping_cart.list_user_shopping_cart_items(user_id)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


#---------- SEARCH APIs ----------#
@app.route('/search/search-item-by-keyword', methods=['GET'])
def search_search_item_by_keyword():
    """
    search-search-item-by-keyword API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: search_search_item_by_keyword
          properties:
            keyword:
              type: string (optional)
    responses:
      200:
        description: Succeeded - searching result is retrieved.
      400:
        description: Failed - searching result is not retrieved.
      data:
        description: Keys - item_list, msg
    """
    keyword = request.args.get('keyword')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.search.search_item_by_keyword(keyword)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/search/search-item-by-category', methods=['GET'])
def search_search_item_by_category():
    """
    search-search-item-by-category API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: search_search_item_by_category
          properties:
            category_id:
              type: integer
    responses:
      200:
        description: Succeeded - searching result is retrieved.
      400:
        description: Failed - searching result is not retrieved.
      data:
        description: Keys - item_list, msg
    """
    category_id = int(request.args.get('category_id'))

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.search.search_item_by_category(category_id)

    if result:
        return jsonify(data), 200
    return jsonify(data), 400


#---------- LOGIN APIs ----------#
@app.route('/login/login', methods=['POST'])
def login_login():
    """
    login-login API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: shopping-cart-add-item-to-user-shopping-cart
          properties:
            email:
              type: integer
            password:
              type: integer
    responses:
      200:
        description: Succeeded - Logged in.
      400:
        description: Failed - Not logged in.
      json:
        description: Keys - is_admin, _id, msg

    """
    username = request.json.get('email')
    password = request.json.get('password')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.login.login(username, password)
    if result:
        return jsonify(data), 200
    return jsonify(data), 400


@app.route('/login/register', methods=['POST'])
def login_register():
    """
    login-register API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: login-register
          properties:
            email:
              type: string
            first_name:
              type: string
            last_name:
              type: string
            password:
              type: string
            is_admin:
              type: bool
    responses:
      200:
        description: Suceeded - User is created.
      400:
        description: Failed - User is existed.
      json:
        description: Keys - _id
    """
    username = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    password = request.json.get('password')
    date_joined = datetime.today().strftime('%Y-%m-%d')
    is_admin = request.json.get('is_admin')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.login.register(username, first_name, last_name, password, date_joined, is_admin)
    if result:
        return data, 200
    return data, 400


@app.route('/login/get-account-info', methods=['POST'])
def login_get_account_info():
    """
    login-login API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: login-get-account-info
          properties:
            account_id:
              type: integer
    responses:
      200:
        description: Succeeded - Info is retrieved.
      400:
        description: Failed - Info is not retrieved.
      json:
        description: Keys - _id, email, first_name, last_name, date_joined, is_admin, msg
    """

    account_id = request.json.get('account_id')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.login.get_account_info(account_id)
        if 'is_admin' in data:
          if data['is_admin']:
            data['email'] = data['admin']
            data.pop('admin')
          else:
            data['email'] = data['username']
            data.pop('username')
        
    if result:
        data.pop('password')
        return jsonify(data), 200
    return jsonify(data), 400








# # TODO
# @app.route('/admin-user-query', methods=['POST'])
# def admin_user_query():
#     """
#     admin-user-query API
#     ---
#     parameters:
#       - name: body
#         in: body
#         required: true
#         schema:
#           id: admin-user-query
#           properties:
#             keyword:
#               type: string
#     responses:
#       200:
#         description: Succeeded - search result returned.
#       400:
#         description: Failed - fail to search.
#     """
#     keyword = request.json.get('keyword')
#     with ClusterRpcProxy(CONFIG) as rpc:
#         search_result, result, msg = rpc.admin.search_user(keyword)
#     if result:
#         return msg, 200
#     return msg, 400





# # TODO
# @app.route('/login-admin-login', methods=['POST'])
# def login_admin_login():
#     """
#     login-admin-login API
#     ---
#     parameters:
#       - name: body
#         in: body
#         required: true
#         schema:
#           id: login-admin-login
#           properties:
#             admin:
#               type: string
#             password:
#               type: string
#     responses:
#       200:
#         description: Succeeded - admin logged in.
#       400:
#         description: Failed - admin failed to login.
#     """
#     admin = request.json.get('admin')
#     password = request.json.get('password')
#     with ClusterRpcProxy(CONFIG) as rpc:
#         result, msg = rpc.login.admin_login(admin, password)
#     if result:
#         return msg, 200
#     return msg, 400


# @app.route('/item-auction-list', methods=['POST'])
# def item_auction_list():
#     """
#     item-auction-list API
#     ---
#     parameters:
#       - name: body
#         in: body
#         required: true
#         schema:
#           id: item-auction-list
#           properties:
#             status:
#               type: string
#     responses:
#       200:
#         description: Succeeded - user succeeded to get item list.
#       400:
#         description: Failed - user failed to get item list..
#     """
#     status = request.json.get('status')
#     with ClusterRpcProxy(CONFIG) as rpc:
#         result, data = rpc.auction.list_item(status)
#     if result:
#         return jsonify(data), 200
#     return {}, 400

# @app.route('/item-auction-update', methods=['POST'])
# def item_auction_update():
#     """
#     item-auction-update API
#     ---
#     parameters:
#       - name: body
#         in: body
#         required: true
#         schema:
#           id: item-auction-update
#           properties:
#             item_id:
#               type: string
#     responses:
#       200:
#         description: Succeeded - auction status is updated.
#       400:
#         description: Failed - no need to update auction status.
#     """
#     item_id = request.json.get('item_id')
#     with ClusterRpcProxy(CONFIG) as rpc:
#         result, status = rpc.auction.update_auction_status(item_id)
#     if result:
#         return status, 200
#     return status, 400


# @app.route('/item-auction-set-window', methods=['POST'])
# def item_auction_set_window():
#     """
#     item-auction-set-window API
#     ---
#     parameters:
#       - name: body
#         in: body
#         required: true
#         schema:
#           id: item-auction-set-window
#           properties:
#             item_id:
#               type: string
#             start_time:
#               type: integer
#             end_time:
#               type: integer
#     responses:
#       200:
#         description: Succeeded - set auction window.
#       400:
#         description: Failed - unable to set auction window.
#     """
#     item_id = request.json.get('item_id')
#     start_time = request.json.get('start_time')
#     end_time = request.json.get('end_time')
#     with ClusterRpcProxy(CONFIG) as rpc:
#         result, msg = rpc.auction.set_auction_window(item_id, start_time, end_time)
#     if result:
#         return msg, 200
#     return msg, 400


# @app.route('/notification-send-email', methods=['POST'])
# def notification_send_email():
#     """
#     notification-send-email API
#     ---
#     parameters:
#       - name: body
#         in: body
#         required: true
#         schema:
#           id: notification-send-email
#           properties:
#             email_address:
#               type: string
#             subject:
#               type: string
#             content:
#               type: string
#     responses:
#       200:
#         description: Succeeded.
#       400:
#         description: Failed.
#     """
#     email_address = request.json.get('email_address')
#     subject = request.json.get('subject')
#     content = request.json.get('content')
#     with ClusterRpcProxy(CONFIG) as rpc:
#         result, msg = rpc.notification.send_email(email_address, subject, content)
#     if result:
#         return msg, 200
#     return msg, 400









app.run(debug=True)

