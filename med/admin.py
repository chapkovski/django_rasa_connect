from django.contrib import admin

# Register your models here.
from django.apps import apps

from .models import Request, Reason

models = apps.get_models()


class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'reason', 'open', 'patient', 'rasa_conversation_id')
    list_display_links = ('id', 'patient')
    list_per_page = 25


class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'body', 'desc')
    list_display_links = ('id', 'body', 'desc')
    list_per_page = 25


admin.site.register(Request, RequestAdmin)
admin.site.register(Reason, ReasonAdmin)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
