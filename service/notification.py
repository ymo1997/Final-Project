from nameko.rpc import rpc, RpcProxy
from mailjet_rest import Client

api_key = '01c8781e582ce292c1db9fae3d494c1c'
api_secret = 'caa00a1184d5714ad2066663fb1aa789'
sender_email = 'yinghuamo.4174@gmail.com'

# https://www.mailjet.com/
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

class Notification(object):
    name = "notification"

    @rpc
    def send_email(self, subject, content):
        api_key = None
        api_secret = None
        data = {
          'Messages': [
            {
              "From": {
                "Email": sender_email,
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