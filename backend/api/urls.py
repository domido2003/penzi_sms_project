from django.urls import path
from . import views

urlpatterns = [
    # Messages list & simulator
    path("sms/", views.message_list_create, name="message_list_create"),

    # SMS command handler
    path("sms/handler/", views.sms_handler, name="sms_handler"),

    # Paginated users list
    path("users/", views.user_list, name="user_list"),

    # Analytics for charts
    path("stats/user-growth/", views.user_growth, name="user_growth"),
    path("stats/message-volume/", views.message_volume, name="message_volume"),
    path("stats/top-counties/", views.top_counties, name="top_counties"),
    path("stats/description-volume/", views.description_volume, name="description_volume"),
]
