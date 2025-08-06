from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    message_list_create,            # Function-based view for messages
    SMSHandlerView,                 # Class-based view for processing SMS
    UserListView,                   # JWT-protected CBV for user list
    UserGrowthChart,                # Analytics views
    MessageVolumeChart,
    TopCountiesChart,
    DescriptionVolumeChart,
)

urlpatterns = [
    path('messages/', message_list_create, name='message_list_create'),
    path('sms/', SMSHandlerView.as_view(), name='sms_handler'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('analytics/user-growth/', UserGrowthChart.as_view(), name='user_growth'),
    path('analytics/message-volume/', MessageVolumeChart.as_view(), name='message_volume'),
    path('analytics/top-counties/', TopCountiesChart.as_view(), name='top_counties'),
    path('analytics/description-volume/', DescriptionVolumeChart.as_view(), name='description_volume'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
