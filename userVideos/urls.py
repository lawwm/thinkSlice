from django.urls import path, include
from .views import UploadVideo, AssetView, GetEditDeleteVideoView, listAllUserVideosView, videoLikesView, videoCommentsView, GetEditDeleteCommentView

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

videoLikesAsView = videoLikesView.as_view({
    'post': 'like',
    'delete': 'unlike'
})

videoCommentsAsView = videoCommentsView.as_view({
    'post': 'addComment',
    'get': 'list'
})

urlpatterns = [
    path('api/videos/assets', UploadVideo, name='direct_url'),
    path('api/videos/assets/<str:upload_id>',
         AssetViewAsView, name="upload_video"),
    path('api/videos/<int:pk>', GetEditDeleteVideoViewAsView, name='handle_video'),
    path('api/videos', listAllUserVideosAsView, name="list_videos"),
    path('api/videos/likes/<int:pk>', videoLikesAsView, name='video_likes'),
    path('api/videos/comments/<int:pk>',
         videoCommentsAsView, name='comment_view'),
    path('api/comments/<int:pk>', GetEditDeleteCommentView.as_view(), name='handle_comment')
]
