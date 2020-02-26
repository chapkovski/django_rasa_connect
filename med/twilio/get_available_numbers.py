# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os

account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_TOKEN']


def get_in_out():
    client = Client(account_sid, auth_token)
    account = client.api.accounts.get(account_sid)
    print(account.balance.fetch().balance)
    inphone = client.incoming_phone_numbers.list()[0].phone_number
    outphone = client.outgoing_caller_ids.list()[0].phone_number
    return inphone, outphone
