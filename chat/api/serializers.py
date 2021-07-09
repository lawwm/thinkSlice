from rest_framework import serializers

from chat.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    recipientName = serializers.CharField(read_only=True, source="recipientProfile.username")
    recipientPic = serializers.URLField(read_only=True, source="recipientProfile.profile_pic")
    class Meta:
        model = Chat
        fields = '__all__'
        