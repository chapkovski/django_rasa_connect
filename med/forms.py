
from django.forms import ModelForm, ChoiceField
from .models import Request
from django.conf import settings
from .twilio import initiate_convo

class RequestForm(ModelForm):
    patient = ChoiceField(choices=[(settings.OUT_PHONE, settings.OUT_PHONE)])

    class Meta:
        model = Request
        fields = ['reason', 'patient']

