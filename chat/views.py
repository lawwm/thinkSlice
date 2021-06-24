from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import ChatRoom

def get_20_messages(chatId, page):
    chat = get_object_or_404(ChatRoom, id=chatId)
    head = page * 20
    tail = (page + 1) * 20
    return chat.messages.order_by('-timestamp').all()[head:tail]