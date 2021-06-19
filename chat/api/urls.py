from django.urls import path

from .views import ChatView, GetEditChatView

ChatAsView = ChatView.as_view({
    'post': 'create',
    'get': 'list',
})

urlpatterns = [
    path('api/chat/<int:pk>', ChatAsView, name='chat_view'),
    path('api/chat/handle/<int:pk>', GetEditChatView.as_view(), name='handle_chat'),
]