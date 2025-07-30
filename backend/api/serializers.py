# backend/api/serializers.py

from rest_framework import serializers
from .models import Message, User, MatchTracking

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'date_created']  # Prevent frontend from trying to override them

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id']  # ID is auto-generated

class MatchTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchTracking
        fields = '__all__'
        read_only_fields = ['id', 'last_updated']
