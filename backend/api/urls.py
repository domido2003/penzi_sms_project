from django.urls import path
from .views import sms_handler, message_list_create, list_users

urlpatterns = [
    path("sms/", sms_handler),  # Already working
    path("messages/", message_list_create),  
    path("users/", list_users),
]
