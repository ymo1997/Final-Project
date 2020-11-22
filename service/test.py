from mailjet_rest import Client
import os

api_key = '0d4dab30fd374a84f21be513f3ebb812'
api_secret = '959c4a451014c6439535f28ce0732012'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "zhan2212@uchicago.edu",
        "Name": "Yueyang"
      },
      "To": [
        {
          "Email": "zyy1996zyy@hotmail.com",
          "Name": "Yueyang"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())