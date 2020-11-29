from mailjet_rest import Client
from config import *

API_KEY = '01c8781e582ce292c1db9fae3d494c1c'
API_SECRET = 'caa00a1184d5714ad2066663fb1aa789'
SENDER_EMAIL = 'yinghuamo.4174@gmail.com'

# https://www.mailjet.com/
mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')

class Notification(object):
    name = NOTIFICATION

    @rpc
    def send_email(self, email_address, subject, content):
        api_key = API_KEY
        api_secret = API_SECRET
        data = {
          'Messages': [
            {
              "From": {
                "Email": SENDER_EMAIL,
                "Name": ""
              },
              "To": [
                {
                  "Email": email_address,
                  "Name": ""
                }
              ],
              "Subject": subject,
              "TextPart": content,
              "HTMLPart": "",
              "CustomID": "AppGettingStartedTest"
            }
          ]
        }
        result = mailjet.send.create(data=data)
        return True, result.json()