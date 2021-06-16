from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import ChatRoom

def get_last_10_messages(chatId):
    chat = get_object_or_404(ChatRoom, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]
