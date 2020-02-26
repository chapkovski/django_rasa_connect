from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.TwilioResponder.as_view(), name='twilio_responder'),
    path('test', views.MedSessionTest.as_view(), name='test'),
    path('new_request', views.NewRequest.as_view(), name='new_request'),
    re_path(r'request/(?P<pk>[0-9]+)', views.IndRequest.as_view(), name='ind_request'),
]