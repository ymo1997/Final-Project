from flask import Flask, request, jsonify
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}

@app.route('/user-register', methods=['POST'])
def user_register():
    """
    user-register API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: user-register
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Succeeded - user registered.
      400:
        description: Failed - user not registered.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.register(username, password)
    if result:
        return msg, 200
    return msg, 400

@app.route('/user-delete', methods=['POST'])
def user_delete():
    """
    user-delete API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: user-delete
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Succeeded - user was deleted.
      400:
        description: Failed - user was not deleted.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.delete_user(username, password)
    if result:
        return msg, 200
    return msg, 400

@app.route('/user-info-edit', methods=['POST'])
def user_info_edit():
    """
    user-info-edit API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: user-info-edit
          properties:
            username:
              type: string
            sex:
              type: string
            age:
              type: integer
    responses:
      200:
        description: Succeeded - user's info changed.
      400:
        description: Failed - user's info not changed.
    """
    username = request.json.get('username')
    sex = request.json.get('sex')
    age = request.json.get('age')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.user.edit_user_info(username, sex, age)
    if result:
        return msg, 200
    return msg, 400

@app.route('/admin-user-create', methods=['POST'])
def admin_user_create():
    """
    admin-user-create API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-user-create
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Succeeded - user created.
      400:
        description: Failed - user not created.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.create_user(username, password)
    if result:
        return msg, 200
    return msg, 400

@app.route('/admin-user-delete', methods=['POST'])
def admin_user_delete():
    """
    admin-user-delete API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-user-delete
          properties:
            username:
              type: string
    responses:
      200:
        description: Succeeded - user deleted.
      400:
        description: Failed - user not deleted.
    """
    username = request.json.get('username')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.delete_user(username)
    if result:
        return msg, 200
    return msg, 400

@app.route('/admin-user-info-edit', methods=['POST'])
def admin_user_info_edit():
    """
    admin-user-info-edit API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-user-info-edit
          properties:
            username:
              type: string
            sex:
              type: string
            age:
              type: integer
    responses:
      200:
        description: Succeeded - user info changed.
      400:
        description: Failed - user info not changed.
    """
    username = request.json.get('username')
    sex = request.json.get('sex')
    age = request.json.get('age')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.edit_user_info(username, sex, age)
    if result:
        return msg, 200
    return msg, 400

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

@app.route('/admin-user-suspend', methods=['POST'])
def admin_user_suspend():
    """
    admin-user-suspend API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: admin-user-suspend
          properties:
            username:
              type: string
    responses:
      200:
        description: Succeeded - user suspended.
      400:
        description: Failed - user not suspended.
    """
    username = request.json.get('username')
    with ClusterRpcProxy(CONFIG) as rpc:
        result, msg = rpc.admin.suspend_user(username)
    if result:
        return msg, 200
    return msg, 400


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


@app.route('/item-bidding-list', methods=['POST'])
def item_bidding_list():
    """
    item-bidding-list API
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: item-bidding-list
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
        result, data = rpc.bidding.list_item(status)
    if result:
        return jsonify(data), 200
    return {}, 400











app.run(debug=True)

