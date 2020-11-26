from nameko.rpc import rpc, RpcProxy
from mailjet_rest import Client


# mailjet = Client(auth=(api_key, api_secret), version='v3.1')

class Notification(object):
    name = "notification"

    

    @rpc
    def send_email(self, email_address, subject, content):
        # https://www.mailjet.com/
        api_key = None
        api_secret = None
        data = {
          'Messages': [
            {
              "From": {
                "Email": "email_address",
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