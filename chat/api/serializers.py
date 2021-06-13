from rest_framework import serializers

from django.contrib.auth.models import User
from chat.models import ChatRoom

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
