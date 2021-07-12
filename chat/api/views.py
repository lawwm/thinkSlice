from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsChatUser
from rest_framework import mixins, generics, viewsets
from rest_framework.response import Response

from userProfiles.models import Profile
from chat.models import ChatRoom, Chat
from .serializers import ChatSerializer


# Create chat with user using their user_id/List all chats started by user_id

class ChatView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        permission_classes = IsAuthenticated

        sender = get_object_or_404(User, id=request.user.id)
        recipient = get_object_or_404(User, id=kwargs['pk'])

        try:
            findExisting = get_object_or_404(
                Chat, sender=sender, recipient=recipient)
            serializer = ChatSerializer(findExisting)
            return Response(serializer.data)

        except:
            chatroom = ChatRoom.objects.create()
            recipientProfile = get_object_or_404(Profile, user=recipient)
            senderProfile = get_object_or_404(Profile, user=sender)

            # Create chat for sender
            request.data['chatroom'] = chatroom.id
            request.data['recipient'] = recipient.id
            request.data['sender'] = sender.id
            request.data['recipientProfile'] = recipientProfile.id
            serializer1 = ChatSerializer(data=request.data)
            serializer1.is_valid(raise_exception=True)
            serializer1.save()

            # Create chat for recipient
            request.data['recipient'] = sender.id
            request.data['sender'] = recipient.id
            request.data['chatroom'] = chatroom.id
            request.data['recipientProfile'] = senderProfile.id
            serializer2 = ChatSerializer(data=request.data)
            serializer2.is_valid(raise_exception=True)
            serializer2.save()

            return Response(serializer1.data)


    def list(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        chats = Chat.objects.filter(
            sender=user).exclude(hidden=True).order_by('-last_modified')
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


# Handle chat using chat_id

class GetEditChatView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        oldChat = get_object_or_404(Chat, id=self.kwargs['pk'])
        request.data["hidden"] = not oldChat.hidden
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        chat = get_object_or_404(Chat, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, chat)
        return chat

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsChatUser]
        return [permission() for permission in permission_classes]


# Update the last_message_count when a chat was read, using chat_id.

class ChatUnreadView(viewsets.ViewSet):

    def updateUnread(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, id=self.kwargs['pk'])
        chat.last_message_count = chat.new_message_count
        chat.save()
        return Response("Chat unread messages updated")
