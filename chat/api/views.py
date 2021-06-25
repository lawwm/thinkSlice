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

        sender = get_object_or_404(Profile, user=request.user.id)
        recipient = get_object_or_404(Profile, user=kwargs['pk'])

        try:
            findExisting = get_object_or_404(
                Chat, sender=sender, recipient=recipient)
            serializer = ChatSerializer(findExisting)
            return Response(serializer.data)

        except:
            chatroom = ChatRoom.objects.create()

            # Create chat for sender
            request.data['chatroom'] = chatroom.id
            request.data['recipient'] = recipient.id
            request.data['sender'] = sender.id
            serializer = ChatSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user.id)
        chats = Chat.objects.filter(
            sender=profile.id).order_by('-date_started')
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)
    

    def startChat(self, request, *args, **kwargs):
        sender = get_object_or_404(Profile, user=request.user.id)
        recipient = get_object_or_404(Profile, user=kwargs['pk'])
        findExisting = get_object_or_404(Chat, sender=sender, recipient=recipient)

        # Create chat for recipient
        request.data['recipient'] = sender.id
        request.data['sender'] = recipient.id
        request.data['chatroom'] = findExisting.chatroom.id
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Chat successfully started with recipient")


# Handle chat using chat_id

class GetEditChatView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        request.data["hidden"] = True
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        chat = get_object_or_404(Chat, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, chat)
        return chat

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsChatUser]
        return [permission() for permission in permission_classes]

# Get chat using chatroom_id

class ChatRoomView(viewsets.ViewSet):
    def retrieve(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated, IsChatUser]

        sender = get_object_or_404(Profile, user=request.user.id)
        chatroom = get_object_or_404(ChatRoom, id=kwargs['pk'])

        chat = get_object_or_404(
                Chat, sender=sender, chatroom=chatroom)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
