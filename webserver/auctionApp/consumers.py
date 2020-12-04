from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import requests
from datetime import timedelta
from datetime import datetime
User = get_user_model()
URL_BASE = "http://172.17.0.3:5000/"

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        room_name = int(data['auction_id'])
        r = requests.get(URL_BASE +
                         "auction/get-auction-history?item_id={}".format(room_name))
        if r is None:
            return
        r_dict = r.json()
        print("DEBUG: AUCTION HISTORY {}".format(r_dict))
        auction_list = r_dict["auction_list"]
        messages = []
        for auction_record in auction_list:
            buyer_id = int(auction_record["auction_user_id"])
            res = requests.post(URL_BASE + "login/get-account-info",
                      json={"account_id": buyer_id})
            if res is None:
                continue
            buyer_dict = res.json()
            if "first_name" not in buyer_dict:
                return 
            price = auction_record["auction_price"]
            auction_time = int(auction_record["auction_time"])
            time_stamp = datetime.fromtimestamp(auction_time)
            messages.append({"price": price,
                            "time_stamp": time_stamp,
                            "buyer": {
                                "id": buyer_id,
                                "first_name": buyer_dict["first_name"],
                                "last_name": buyer_dict["last_name"],
                            }})
        print(messages)
        content = {
            'messages': self.messages_to_json(messages),
            'command': 'messages'
        }
        self.send_message(content)
        pass

    def new_message(self, data):
        sender_id = int(data['from'])
        auction_id = int(data['auction_id'])
        price = int(float(data['price']))
        r = requests.post(URL_BASE + "login/get-account-info",
            json={"account_id": sender_id})
        if r is None:
            return print("new message seller is invalid")
        r_dict = r.json()
        first_name = r_dict["first_name"]
        last_name = r_dict["last_name"]
        sender = {
            "id": sender_id,
            "first_name": first_name,
            "last_name": last_name
        }
        message = {
            "buyer": sender,
            "price": price,
            "time_stamp": datetime.now()
        }
        res = requests.post(URL_BASE + "auction/bid-item",
                            json = {"auction_price": int(price),
                                    "auction_user_id": sender_id,
                                    "item_id": auction_id})
        if res is None:
            print("DEBUG: BID ITEM FAILED")
            return
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def fetch_items(self, data):
        sender_id = int(data['from'])
        res = requests.get(URL_BASE +
                           "shopping-cart/list-user-shopping-cart-items" +
                           "?user_id={}".format(sender_id))
        if res is None:
            return
        res_dict = res.json()
        items = []
        if type(res_dict) is dict:
            items = self.items_to_json(res_dict["item_list"])
        content = {
            'items': items,
            'command': 'items'
        }
        self.send_message(content)

    def new_item(self, data):
        sender_id = int(data['from'])
        item_id = int(data['auction_id'])
        content = {
            'command': 'new_item',
            'item': self.item_to_json(item_id),
            'from': sender_id
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message["buyer"]["id"],
            'sender': message["buyer"]["first_name"] + " " + message["buyer"]["last_name"],
            'profile_image': "/media/profile_images/profilepic.jpg",
            'price': message["price"],
            'timestamp': str(message["time_stamp"].strftime('%Y-%m-%d %H:%M:%S')),
        }

    def items_to_json(self, item_ids):
        result = []
        for item_id in item_ids:
            result.append(self.item_to_json(item_id))
        return result

    def item_to_json(self, item_id):
        res = requests.post(URL_BASE + "item/get-item-info",
                            json={"item_id": item_id})
        if res is None:
            print("ERROR: ITEM ID is invalid.")
            return {}
        res_dict = res.json()
        return {
            'name': res_dict.get("item_name"),
            'item_image': res_dict.get("image_url"),
            'price': res_dict.get("current_auction_price"),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'fetch_items': fetch_items,
        'new_item': new_item,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        if data['command'] in self.commands:
            self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
