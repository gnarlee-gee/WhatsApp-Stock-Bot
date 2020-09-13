# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get("Body", "").strip().lower()
    remote_number = request.values.get("From", "")
    output_lines = []
    print(remote_number)
    # incoming From is "whatsapp:#######"
    if remote_number.startswith("whatsapp:"):
        remote_number = remote_number.split(":")[1]

    if not remote_number:
        remote_number = "123"
    print(remote_number)  # remote_number is human's number

    # incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run()


# import os


# # Your Account Sid and Auth Token from twilio.com/console
# # DANGER! This is insecure. See http://twil.io/secure
# account_sid = os.getenv("TWILIO_ACCOUNT_SID")
# auth_token = os.getenv("TWILIO_ACCOUNT_AUTH")

# print(account_sid)
# print(auth_token)
# client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                     from_=os.getenv("TWILIO_ACCOUNT_PHONENUM"),
#                     to=os.getenv("MY_PHONE_NUM")
#                 )

# print(message.sid)
