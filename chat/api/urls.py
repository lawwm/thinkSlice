from django.urls import path

from .views import ChatRoomView, ChatView, GetEditChatView

ChatAsView = ChatView.as_view({
    'post': 'create',
    'get': 'list',
    'patch': 'startChat',
})

ChatRoomAsView = ChatRoomView.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('api/chat/<int:pk>', ChatAsView, name='chat_view'),
    path('api/chat/handle/<int:pk>', GetEditChatView.as_view(), name='handle_chat'),
    path('api/chat/chatroom/<int:pk>', ChatRoomAsView, name='chatroom_view'),
]
