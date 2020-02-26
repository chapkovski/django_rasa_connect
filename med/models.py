from django.db import models
from django.conf import settings
from uuid import uuid4


reasons = [(i['reason'], i['description']) for i in settings.REASONS]


# Ph Ch: IRL should be match between pations and reasons.
# in our case we'll just take the in and out phones from .ENV files
# and reasons from yaml


# class Patient(models.Model):
#     phone = models.IntegerField()
#
class Answer(models.Model):
    pass


class Reason(models.Model):
    body = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.body


class Request(models.Model):
    class Meta:
        get_latest_by = 'created_at'

    reason = models.ForeignKey(to=Reason, on_delete=models.CASCADE)  # PHCH: again in IRL we need to use foreignkeys hee
    # patient = models.ForeignKey(to=Patient, on_delete=models.CASCADE)
    rasa_conversation_id = models.CharField(max_length=100, unique=True, editable=False)
    patient = models.CharField(max_length=100, default=settings.OUT_PHONE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return f'TO: {self.patient}; REASON: {self.reason}'
