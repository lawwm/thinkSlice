from django.urls import path

from .views import ChatRoomView, CreateChatRoomView

CreateChatRoomAsView = CreateChatRoomView.as_view({
    'post': 'create'
})

urlpatterns = [
    path('api/chat/<int:pk>', ChatRoomView.as_view(), name='handle_chat'),
    path('api/chat/create/<int:pk>', CreateChatRoomAsView, name='create_chat'),
]