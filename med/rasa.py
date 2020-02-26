import requests
from django.conf import settings
import json


class RasaResponse:
    def __init__(self, resp):
        print("RAW::", resp)
        single_resp = resp[0]
        custom_resp = single_resp.get('custom')
        if custom_resp:
            self.text = custom_resp.get('text')
            self.open = custom_resp.get('status') != 'over'
            return
        if single_resp.get('text'):
            self.text = single_resp.get('text')
            self.open = True

    def __str__(self):
        return f'Open:: {self.open}; TEXT:: {self.text}'


def send_to_rasa(msg, channel):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = json.dumps(dict(sender=channel, message=msg))
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    rasa_response = json.loads(response.text)
    return RasaResponse(rasa_response)


def trigger_intend(intend, channel, reason):
    url = f"http://localhost:5005/conversations/{channel}/trigger_intent"
    payload = json.dumps(dict(name=intend,
                              entities=dict(reason=reason)))
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    rasa_response = json.loads(response.text)
    messages = rasa_response.get('messages')
    if messages and isinstance(messages, list) and len(messages)>0:
        message = messages[0]
        custom = message.get('custom')
        raw_text = message.get('text')
        if custom and custom.get('text'):
            return custom.get('text')
        return raw_text



if __name__ == '__main__':
    print(trigger_intend('wellness_check', 'asdf'))
