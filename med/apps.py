from django.apps import AppConfig
from django.conf import settings

class MedConfig(AppConfig):
    name = 'med'

    def ready(self):
        from .models import Reason
        for i in settings.REASONS:
            Reason.objects.get_or_create(body=i['reason'], defaults={'desc':i['description']})
        from . import signals

