from django.conf import settings
from twilio.rest import Client

account_sid = settings.TWILIO_SID
auth_token = settings.TWILIO_TOKEN
from_phone = settings.IN_PHONE


def initiate_convo(request, intro):
    client = Client(account_sid, auth_token)
    client.messages.create(body=intro, from_=from_phone, to=request.patient)
