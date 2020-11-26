from flask import Flask, request, jsonify
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

#---------- CONFIG ----------#
app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


#---------- USER APIs ----------#
@app.route('/user/create-account', methods=['POST'])
def user_create_account():
    """
    /user/create-account API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: user-create-account
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Suceeded - User is created.
      400:
        description: Failed - User is existed.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.create_account(username, password)
    if result:
        return msg, 200
    return msg, 400


@app.route('/user/update-account-info', methods=['POST'])
def user_update_account_info():
    """
    /user/update-account-info API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: user-update-account-info
          properties:
            username:
              type: string
            sex:
              type: string
            age:
              type: integer
    responses:
      200:
        description: Suceeded - User info is changed.
      400:
        description: Failed - User info is not changed.
    """
    username = request.json.get('username')
    sex = request.json.get('sex')
    age = request.json.get('age')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.update_account_info(username, sex, age)
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
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Succeeded - user is deleted.
      400:
        description: Failed - user is not deleted.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.delete_account(username, password)
    if result:
        return msg, 200
    return msg, 400


#---------- USER APIs ----------#
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
    responses:
      200:
        description: Succeeded - user is created.
      400:
        description: Failed - user is not created.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.create_user_account(username, password)
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
            username:
              type: string
    responses:
      200:
        description: Succeeded - user is deleted.
      400:
        description: Failed - user is not deleted.
    """
    username = request.json.get('username')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.delete_user_account(username)
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
            username:
              type: string
            sex:
              type: string
            age:
              type: integer
    responses:
      200:
        description: Succeeded - user info is changed.
      400:
        description: Failed - user info is not changed.
    """
    username = request.json.get('username')
    sex = request.json.get('sex')
    age = request.json.get('age')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.update_user_account_info(username, sex, age)
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
            username:
              type: string
    responses:
      200:
        description: Succeeded - user is suspended.
      400:
        description: Failed - user is not suspended.
    """
    username = request.json.get('username')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.suspend_user_account(username)
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
          id: admin-suspend-user-account
          properties:
            item_name:
              type: string
            seller_id:
              type: integer
            category_name:
              type: string
            description:
              type: string
            auction_start_time:
              type: integer
            auction_end_time:
              type: integer
            starting_price:
              type: float
    responses:
      200:
        description: Succeeded - item is created.
      400:
        description: Failed - item is not created.
    """
    item_name = request.json.get('item_name')
    seller_id = request.json.get('seller_id')
    category_name = request.json.get('category_name')
    description = request.json.get('description')
    auction_start_time = request.json.get('auction_start_time')
    auction_end_time = request.json.get('auction_end_time')
    starting_price = request.json.get('starting_price')

    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.item.create_item(item_name, 
        seller_id, category_name, description, 
        auction_start_time, auction_end_time,
        starting_price)
    if result:
        return msg, 200
    return msg, 400



# TODO
@app.route('/admin-user-query', methods=['POST'])
def admin_user_query():
    """
    admin-user-query API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-user-query
          properties:
            keyword:
              type: string
    responses:
      200:
        description: Succeeded - search result returned.
      400:
        description: Failed - fail to search.
    """
    keyword = request.json.get('keyword')
    with ClusterRpcProxy(CONFIG) as rpc:
        search_result, result, msg = rpc.admin.search_user(keyword)
    if result:
        return msg, 200
    return msg, 400





# TODO
@app.route('/login-admin-login', methods=['POST'])
def login_admin_login():
    """
    login-admin-login API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: login-admin-login
          properties:
            admin:
              type: string
            password:
              type: string
    responses:
      200:
        description: Succeeded - admin logged in.
      400:
        description: Failed - admin failed to login.
    """
    admin = request.json.get('admin')
    password = request.json.get('password')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.login.admin_login(admin, password)
    if result:
        return msg, 200
    return msg, 400


@app.route('/item-auction-list', methods=['POST'])
def item_auction_list():
    """
    item-auction-list API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item-auction-list
          properties:
            status:
              type: string
    responses:
      200:
        description: Succeeded - user succeeded to get item list.
      400:
        description: Failed - user failed to get item list..
    """
    status = request.json.get('status')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, data = rpc.auction.list_item(status)
    if result:
        return jsonify(data), 200
    return {}, 400

@app.route('/item-auction-update', methods=['POST'])
def item_auction_update():
    """
    item-auction-update API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item-auction-update
          properties:
            item_id:
              type: string
    responses:
      200:
        description: Succeeded - auction status is updated.
      400:
        description: Failed - no need to update auction status.
    """
    item_id = request.json.get('item_id')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, status = rpc.auction.update_auction_status(item_id)
    if result:
        return status, 200
    return status, 400


@app.route('/item-auction-set-window', methods=['POST'])
def item_auction_set_window():
    """
    item-auction-set-window API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item-auction-set-window
          properties:
            item_id:
              type: string
            start_time:
              type: integer
            end_time:
              type: integer
    responses:
      200:
        description: Succeeded - set auction window.
      400:
        description: Failed - unable to set auction window.
    """
    item_id = request.json.get('item_id')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.auction.set_auction_window(item_id, start_time, end_time)
    if result:
        return msg, 200
    return msg, 400


@app.route('/notification-send-email', methods=['POST'])
def notification_send_email():
    """
    notification-send-email API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: notification-send-email
          properties:
            email_address:
              type: string
            subject:
              type: string
            content:
              type: string
    responses:
      200:
        description: Succeeded.
      400:
        description: Failed.
    """
    email_address = request.json.get('email_address')
    subject = request.json.get('subject')
    content = request.json.get('content')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.notification.send_email(email_address, subject, content)
    if result:
        return msg, 200
    return msg, 400









app.run(debug=True)

