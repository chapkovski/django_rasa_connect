from django.shortcuts import render
import json
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from .generic_classes import TemplateMixin
from django.views.generic.detail import SingleObjectMixin

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from twilio.twiml.messaging_response import (
    MessagingResponse,
    Message,
    Body,
    Media
)
from django.http import HttpResponse, JsonResponse
import requests
from .twilio.get_available_numbers import get_in_out
from .forms import RequestForm
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .models import Request
from django.conf import settings
from .rasa import send_to_rasa
from django.db.models import Q


class MedSessionTest(View):
    def post(self, request, *args, **kwargs):
        if request.session['counter'] >= 10: request.session.clear()
        if request.session.get('counter') is None:
            request.session['counter'] = 0
            print('assigning counter')
        else:
            request.session['counter'] += 1
        print('COUNTER', request.session.get('counter'))
        inphone, outphone = get_in_out()
        return JsonResponse({'inphone': inphone, 'outphone': outphone})


class TwilioResponder(View):
    @staticmethod
    def get_open_request(phone=None, rasa_conversation_id=None):
        req_obj_q = Request.objects.filter(open=True).filter(
            Q(rasa_conversation_id=rasa_conversation_id) | Q(patient=phone))
        if req_obj_q.exists():
            return req_obj_q.latest()

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        resp = MessagingResponse()
        rasa_conversation_id = request.session.get('rasa_conversation_id')
        patient_phone_number = request.POST.get('From')
        user_response = request.POST.get('Body')
        not_found_msg = 'I cannot give you any information now... sorry!'
        open_request = self.get_open_request(phone=patient_phone_number, rasa_conversation_id=rasa_conversation_id)
        if open_request:
            rasa_resp = send_to_rasa(msg=user_response, channel=open_request.rasa_conversation_id)
            resp.message(rasa_resp.text)
            open_request.open = rasa_resp.open
            open_request.save()
        else:
            resp.message(not_found_msg)
        return HttpResponse(str(resp))


class NewRequest(CreateView):
    form_class = RequestForm
    template_name = 'med/request_form.html'

    def get_context_data(self, **kwargs):
        r = super().get_context_data(**kwargs)
        r = {**dict(inphone=settings.IN_PHONE,
                    outphone=settings.OUT_PHONE), **r}
        return r

    def get_success_url(self):
        return reverse('ind_request', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        r = super().form_valid(form)
        return r


class IndRequest(DetailView):
    model = Request
