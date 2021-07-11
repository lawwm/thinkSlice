from django.urls import path

from .views import ChatView, GetEditChatView, ChatUnreadView

ChatAsView = ChatView.as_view({
    'post': 'create',
    'get': 'list',
})

ChatUnreadAsView = ChatUnreadView.as_view({
    'patch': 'updateUnread',
})

urlpatterns = [
    path('api/chat/<int:pk>', ChatAsView, name='chat_view'),
    path('api/chat/handle/<int:pk>', GetEditChatView.as_view(), name='handle_chat'),
    path('api/chat/unread/<int:pk>', ChatUnreadAsView, name='chat_unread_view')
]
