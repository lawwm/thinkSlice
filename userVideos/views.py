from django.db.models.fields import CharField
from django.shortcuts import get_object_or_404
from mux_python.models.asset import Asset
from rest_framework import serializers, viewsets, status, mixins, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import mux_python
from .serializers import UploadResponseSerializer, CreateVideoSerializer, DisplayVideoSerializer, DisplayLikedVideoSerializer, LikeVideoSerializer, LikedVideoDisplaySerializer, VideoCommentSerializer, AccessCommentSerializer
from django.contrib.auth.models import User
from userProfiles.models import Profile
from .models import Video, VideoComments, VideoLikes, Similarity
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import IsVideoOwnerOrReadOnly, IsCommentOwnerOrReadOnly
from appmanager.settings import MUX_TOKEN_SECRET, MUX_TOKEN_ID
from mux_python.rest import NotFoundException
from django.db import models
from django.db.models.functions import Greatest
from django.db.models import Q
# Create your views here.

# Create direct url


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def UploadVideo(request):
    # Create video
    if request.method == 'POST':

        # Authentication Setup
        configuration = mux_python.Configuration()
        configuration.username = MUX_TOKEN_ID
        configuration.password = MUX_TOKEN_SECRET

        # API Client Initialization
        uploads_api = mux_python.DirectUploadsApi(
            mux_python.ApiClient(configuration))

        # Return url api for direct upload
        create_asset_request = mux_python.CreateAssetRequest(
            playback_policy=[mux_python.PlaybackPolicy.PUBLIC])
        create_upload_request = mux_python.CreateUploadRequest(timeout=3600, new_asset_settings=create_asset_request,
                                                               cors_origin="thinkslice.vercel.app", test=False)
        create_upload_response = uploads_api.create_direct_upload(
            create_upload_request)

        print(create_upload_response)
        serialized = UploadResponseSerializer(create_upload_response.data)
        return Response(serialized.data)

# Upload video to mux using direct url


class AssetView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Authentication Setup
        configuration = mux_python.Configuration()
        configuration.username = MUX_TOKEN_ID
        configuration.password = MUX_TOKEN_SECRET

        # API Clients Initialization
        uploads_api = mux_python.DirectUploadsApi(
            mux_python.ApiClient(configuration))
        assets_api = mux_python.AssetsApi(mux_python.ApiClient(configuration))

        # GET asset_id to query asset
        upload_response = uploads_api.get_direct_upload(kwargs['upload_id'])
        if upload_response.data.status != 'asset_created':
            return Response("The video was not successfully uploaded, please try again.",
                            status=status.HTTP_404_NOT_FOUND)
        asset_id = upload_response.data.asset_id

        # GET asset using asset_id
        asset_response = assets_api.get_asset(asset_id)
        print(asset_response)
        print(asset_response.data.duration)
        print(request.data)

        # Append API data to request data
        request.data['creator_profile'] = get_object_or_404(
            Profile, user=request.user.id).id
        request.data['asset_id'] = asset_id
        request.data['playback_id'] = asset_response.data.playback_ids[0].id
        #request.data['duration'] = asset_response.data.duration
        request.data['policy'] = asset_response.data.playback_ids[0].policy
        request.data['created_at'] = asset_response.data.created_at

        print(request.data)

        # Check if same profile has created a video for the same subject
        check_existing = Video.objects.filter(creator_profile=request.data['creator_profile'],
                                              subject=request.data['subject'])
        if check_existing.exists():
            return Response("You've already created a video for this particular subject",
                            status=status.HTTP_400_BAD_REQUEST)

        # Create serializer
        serializer = CreateVideoSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# Get/Edit/Delete a video from video_id
class GetEditDeleteVideoView(viewsets.ViewSet):

    def retrieve(self, request, *args, **kwargs):
        video = get_object_or_404(Video, pk=self.kwargs['pk'])
        video.views = video.views + 1
        video.save()
        check_existing = VideoLikes.objects.filter(liked_video=self.kwargs['pk'], 
                                                user_liking=request.user.id)
        if check_existing.exists():
            video.hasUserLiked = True
        else :
            video.hasUserLiked = False
        
        serializer = DisplayLikedVideoSerializer(video)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        video = get_object_or_404(Video, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, video)
        serializer = DisplayVideoSerializer(
            video, data=request.data, partial=True, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Call to API
        # Authentication Setup
        configuration = mux_python.Configuration()
        configuration.username = MUX_TOKEN_ID
        configuration.password = MUX_TOKEN_SECRET

        # API Client Initialization
        assets_api = mux_python.AssetsApi(mux_python.ApiClient(configuration))

        # Delete asset_id
        video = get_object_or_404(Video, pk=self.kwargs['pk'])

        # Check that asset is gone
        try:
            assets_api.delete_asset(video.asset_id)
            deletedVideo = video.delete()
            print(deletedVideo)
            return Response("Video successfully deleted", status=status.HTTP_200_OK)
        except NotFoundException as e:
            assert e != None
            return Response("Asset does not exist", status=status.HTTP_424_FAILED_DEPENDENCY)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsVideoOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

# Get 10 videos ordered either by views or data
# Query videos from numbers
# n is the set of 9 videos
# Either filter by 'created_at' or 'views'
# ascending is boolean, so either 'true' or 'false'


class listAllUserVideosView(viewsets.ViewSet):
    def list(self, request):
        # Get query params
        subject = request.GET.get('subject', None)
        location = request.GET.get('location', None)
        star_upper_limit = request.GET.get('star_upper_limit', None)
        star_lower_limit = request.GET.get('star_lower_limit', None)
        available = request.GET.get('available', None)
        limit_n = request.GET.get('n', 1)
        filter_by = request.GET.get('filter_by', 'created_at')
        ascending = request.GET.get('ascending', 'true')
        index_tail = int(limit_n) * 9
        index_head = index_tail - 9
        if ascending != 'true':
            filter_by = '-' + filter_by

        # Append to filter criteria
        q = Q()
        if subject != None:
            q &= Q(subject__icontains=subject)
        if location != None:
            q &= Q(creator_profile__location__icontains=location)
        if star_upper_limit != None:
            q &= Q(creator_profile__aggregate_star__lte=star_upper_limit)
        if star_lower_limit != None:
            q &= Q(creator_profile__aggregate_star__gte=star_lower_limit)
        if available != None:
            q &= Q(creator_profile__available=available)

        # Return filtered videos
        videos = Video.objects.select_related('creator_profile').filter(q).order_by(filter_by)[index_head:index_tail]
        serializer = DisplayVideoSerializer(videos, many=True)
        return Response(serializer.data)

# Like a video from video_id


class videoLikesView(viewsets.ViewSet):

    def list(self, request, **kwargs):
        videos = VideoLikes.objects.filter(user_liking=kwargs['pk'])
        serializer = LikedVideoDisplaySerializer(videos, many=True)
        return Response(serializer.data)

    def like(self, request, *args, **kwargs):
        # Check if same profile has liked the same video
        check_existing = VideoLikes.objects.filter(liked_video=kwargs['pk'], user_liking=request.user.id)
        if check_existing.exists():
            return Response("You've already liked this particular video",
                            status=status.HTTP_400_BAD_REQUEST)

        # create VideoLikes object
        request.data['liked_video'] = kwargs['pk']
        request.data['user_liking'] = get_object_or_404(
            User, id=request.user.id).id
        serializer = LikeVideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Increment likes on video
        video = get_object_or_404(Video, id=kwargs['pk'])
        video.likes = video.likes + 1
        video.save()
        return Response(serializer.data)

    def unlike(self, request, *args, **kwargs):
        like = get_object_or_404(
            VideoLikes, liked_video=kwargs['pk'], user_liking=request.user.id)
        video = get_object_or_404(Video, id=kwargs['pk'])
        try:
            unliked = like.delete()
            print(unliked)
            video.likes = video.likes - 1
            video.save()
            return Response("Like removed", status=status.HTTP_200_OK)
        except NotFoundException as e:
            assert e != None
            return Response("Video or like does not exist", status=status.HTTP_424_FAILED_DEPENDENCY)

# Comment on a video from video_id


class videoCommentsView(viewsets.ViewSet):

    def addComment(self, request, *args, **kwargs):
        video = get_object_or_404(
            Video, id=kwargs['pk'])
        request.data['commented_video'] = video.id
        request.data['user_commenting'] = get_object_or_404(
            Profile, user_id=request.user.id).id
        serializer = VideoCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        video.num_of_comments = video.num_of_comments + 1
        video.save()
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        comments = VideoComments.objects.filter(commented_video=kwargs['pk'], parent_comment=None).order_by('-date_comment_edited')
        serializer = VideoCommentSerializer(comments, many=True)
        return Response(serializer.data)

# Get the replies to a comment

class commentRepliesView(viewsets.ViewSet):

    def reply(self, request, *args, **kwargs):
        comment = get_object_or_404(VideoComments, id=kwargs['pk'])
        video = get_object_or_404(Video, id=comment.commented_video.id)
        request.data['commented_video'] = video.id
        request.data['parent_comment'] = comment.id
        request.data['user_commenting'] = get_object_or_404(
            Profile, user_id=request.user.id).id
        serializer = VideoCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if (not comment.has_replies):
            comment.has_replies = True
            comment.save()
        video.num_of_comments = video.num_of_comments + 1
        video.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        comment_id = get_object_or_404(VideoComments, id=kwargs['pk']).id
        replies = VideoComments.objects.filter(parent_comment=comment_id).order_by('-date_comment_edited')
        serializer = VideoCommentSerializer(replies, many=True)
        return Response(serializer.data)

# Get/Edit/Delete one comment


class GetEditDeleteCommentView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = AccessCommentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(VideoComments, id=kwargs['pk'])
        video = get_object_or_404(Video, id=comment.commented_video.id)
        video.num_of_comments = video.num_of_comments - 1
        video.save()
        if (not comment.parent_comment == None):
            parent_comment = get_object_or_404(VideoComments, id=comment.parent_comment.id)
            reply_count = VideoComments.objects.filter(parent_comment=parent_comment.id).count()
            if (reply_count == 1):
                parent_comment.has_replies = 0
                parent_comment.save()
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print(request.data)
        request.data["edited"] = True
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        comment = get_object_or_404(VideoComments, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, comment)
        return comment

    def get_permissions(self):

        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsCommentOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


class SearchVideoView(viewsets.ViewSet):
    def list(self, request):
        # Get query params
        search_name = request.GET.get('name', None)
        limit_n = request.GET.get('n', 1)
        filter_by = request.GET.get('filter_by', 'created_at')
        ascending = request.GET.get('ascending', 'true')

        subject = request.GET.get('subject', None)
        location = request.GET.get('location', None)
        star_upper_limit = request.GET.get('star_upper_limit', None)
        star_lower_limit = request.GET.get('star_lower_limit', None)
        available = request.GET.get('available', None)

        # Append to filter criteria
        q = Q()
        if subject != None:
            q &= Q(subject__icontains=subject)
        if location != None:
            q &= Q(creator_profile__location__icontains=location)
        if star_upper_limit != None:
            q &= Q(creator_profile__aggregate_star__lte=star_upper_limit)
        if star_lower_limit != None:
            q &= Q(creator_profile__aggregate_star__gte=star_lower_limit)
        if available != None:
            q &= Q(creator_profile__available=available)

        # Refine inputs
        if ascending != 'true':
            filter_by = '-' + filter_by
        index_tail = int(limit_n) * 9
        index_head = index_tail - 9

        if search_name == None:
            return Response('No input was detected.', status=400)
        videos = Video.objects.select_related('creator_profile').annotate(
            match=Greatest(
                Similarity("video_title", models.Value(search_name)), 
                Similarity("creator_profile__username", models.Value(search_name)),
                output_field=CharField()
            )
        ).filter(q).filter(match__gt=0.20).order_by(filter_by)[index_head:index_tail]
        serializers = DisplayVideoSerializer(videos, many=True)
        return Response(serializers.data)

class FilterVideoView(viewsets.ViewSet):
    def list(self, request):
        subject = request.GET.get('subject', None)
        location = request.GET.get('location', None)
        star_upper_limit = request.GET.get('star_upper_limit', None)
        star_lower_limit = request.GET.get('star_lower_limit', None)
        q = Q()
        if subject != None:
            q &= Q(subject__icontains=subject)
        if location != None:
            q &= Q(creator_profile__location__icontains=location)
        if star_upper_limit != None:
            q &= Q(creator_profile__aggregate_star__lte=star_upper_limit)
        if star_lower_limit != None:
            q &= Q(creator_profile__aggregate_star__gte=star_lower_limit)
        videos = Video.objects.filter(q)
        serializers = DisplayVideoSerializer(videos, many=True)
        return Response(serializers.data)