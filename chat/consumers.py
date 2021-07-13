from chat.api.serializers import ChatSerializer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q

import json

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Chat, Message, ChatRoom
from .views import get_20_messages


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            "chat",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "chat",
            self.channel_name
        )

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.user.id,
            'content': message.message,
            'timestamp': str(message.timestamp)
        }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def fetch_messages(self, data):
        messages = get_20_messages(data['chatroom'], 0)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages),
            'chatroom': data['chatroom']
        }
        self.send_message(content)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            "chat",
            {
                "type": "chat_message",
                "message": message
            }
        )

    def new_message(self, data):
        author = get_object_or_404(User, id=data['from'])
        message = Message.objects.create(
            user=author,
            message=data['message'])
        current_chatroom = get_object_or_404(ChatRoom, id=data['chatroom'])
        current_chatroom.messages.add(message)
        current_chatroom.save()

        current_chat = get_object_or_404(Chat, sender=author, chatroom=current_chatroom)
        current_chat.save()

        recipient_chat = get_object_or_404(Chat, ~Q(sender=author.id), chatroom=current_chatroom.id)
        recipient_chat.new_message_count = recipient_chat.new_message_count + 1
        is_hidden = recipient_chat.hidden
        if (is_hidden):
            recipient_chat.hidden = False
        recipient_chat.save()

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message),
            'chatroom': current_chatroom.id,
            'recipient': data['to']
        }
        if (data['isFirst'] or is_hidden):
            serializer = ChatSerializer(recipient_chat)
            content['chat'] = serializer.data
        return self.send_chat_message(content)

    def more_messages(self, data):
        messages = get_20_messages(data['chatroom'], data['page'])
        content = {
            'command': 'more_messages',
            'messages': self.messages_to_json(messages),
            'chatroom': data['chatroom'],
        }
        self.send_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'more_messages': more_messages
    }

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print(message)
        self.send(text_data=json.dumps(message))
