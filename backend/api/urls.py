from django.urls import path
from . import views

urlpatterns = [
    path("messages/", views.message_list_create),
    path("sms/", views.sms_handler),
    path("users/", views.user_list),  # ✅ Added route
]
