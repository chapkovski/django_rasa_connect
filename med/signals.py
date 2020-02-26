from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Request
from .twilio import initiate_convo
from uuid import uuid4
from .rasa import trigger_intend


@receiver(pre_save, sender=Request)
def generating_rasa_id(sender, instance, *args, **kwargs):
    instance.rasa_conversation_id = instance.rasa_conversation_id or uuid4()


@receiver(post_save, sender=Request)
def sending_trigger_to_user(sender, instance, created, **kwargs):
    if created:
        print('BODY',instance.reason.body)
        intro = trigger_intend('wellness_check',
                               instance.rasa_conversation_id,
                               instance.reason.body)  # TODO: trigger based on request property; not hardcode it
        print("INTROO", intro)
        initiate_convo(instance, intro)
