from django.urls import path, include
from .views import UploadVideo, AssetView, GetEditDeleteVideoView, listAllUserVideosView

AssetViewAsView = AssetView.as_view({
    'post': 'create'
})

GetEditDeleteVideoViewAsView = GetEditDeleteVideoView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

listAllUserVideosAsView = listAllUserVideosView.as_view({
    'get': 'list'
})

urlpatterns = [ 
    path('api/videos/assets', UploadVideo, name='direct_url'),
    path('api/videos/assets/<str:upload_id>', AssetViewAsView, name="upload_video"),
    path('api/videos/<int:pk>', GetEditDeleteVideoViewAsView, name='handle_video'),
    path('api/videos', listAllUserVideosAsView, name="list_videos")
]