from rest_framework import serializers

from chat.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    senderName = serializers.CharField(read_only=True, source="sender.username")
    senderPic = serializers.URLField(read_only=True, source="sender.profile_pic")
    senderId = serializers.IntegerField(read_only=True, source="sender.user.id")

    recipientName = serializers.CharField(read_only=True, source="recipient.username")
    recipientPic = serializers.URLField(read_only=True, source="recipient.profile_pic")
    recipientId = serializers.IntegerField(read_only=True, source="recipient.user.id")

    class Meta:
        model = Chat
        fields = '__all__'