from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsChatOwner, IsChatUser
from rest_framework import mixins, generics, viewsets
from rest_framework.response import Response

from chat.models import ChatRoom
from .serializers import ChatRoomSerializer

class CreateChatRoomView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        permission_classes = IsAuthenticated
        request.data['recipient'] = kwargs['pk']
        request.data['owner'] = request.user.id
        serializer = ChatRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ChatRoomView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ChatRoomSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        chatRoom = get_object_or_404(ChatRoom, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, chatRoom)
        return chatRoom
    
    def get_permissions(self):

        if self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsChatOwner]
        else:
            permission_classes = [IsAuthenticated, IsChatUser]
        return [permission() for permission in permission_classes]