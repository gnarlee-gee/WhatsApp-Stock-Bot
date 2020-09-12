# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_ACCOUNT_AUTH")

print(account_sid)
print(auth_token)
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                    body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                    from_=os.getenv("TWILIO_ACCOUNT_PHONENUM"),
                    to=os.getenv("MY_PHONE_NUM")
                )

print(message.sid)
