from django.shortcuts import get_object_or_404
from mux_python.models.asset import Asset
from rest_framework import serializers, viewsets, status, mixins, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import mux_python 
from .serializers import UploadResponseSerializer, CreateVideoSerializer, DisplayVideoSerializer
from userProfiles.models import Profile
from .models import Video
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import IsVideoOwnerOrReadOnly
from appmanager.settings import MUX_TOKEN_SECRET, MUX_TOKEN_ID
from mux_python.rest import NotFoundException

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
        uploads_api = mux_python.DirectUploadsApi(mux_python.ApiClient(configuration))
        
        # Return url api for direct upload
        create_asset_request = mux_python.CreateAssetRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC])
        create_upload_request = mux_python.CreateUploadRequest(timeout=3600, new_asset_settings=create_asset_request,
             cors_origin="thinkslice.vercel.app", test=True)
        create_upload_response = uploads_api.create_direct_upload(create_upload_request)  
        
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
        uploads_api = mux_python.DirectUploadsApi(mux_python.ApiClient(configuration))
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
        request.data['creator_profile'] = get_object_or_404(Profile, user=request.user.id).id
        request.data['asset_id'] = asset_id
        request.data['playback_id'] = asset_response.data.playback_ids[0].id
        #request.data['duration'] = asset_response.data.duration
        request.data['policy'] = asset_response.data.playback_ids[0].policy
        request.data['created_at'] = asset_response.data.created_at

        print(request.data)

        # Check if same profile has created a video for the same subject
        check_existing = Video.objects.filter(creator_profile = request.data['creator_profile'], 
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
        print(self.request.method)
        video = get_object_or_404(Video, pk=self.kwargs['pk'])   
        video.views = video.views + 1
        video.save()
        serializer = DisplayVideoSerializer(video)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        video = get_object_or_404(Video, pk=self.kwargs['pk'])  
        self.check_object_permissions(self.request, video)
        serializer = DisplayVideoSerializer(video, data = request.data, partial=True, many=False)
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
#     serializer_class = ProfileVideoSerializer
    def list(self, request):
        limit_n = request.GET.get('n', 1)
        filter_by = request.GET.get('filter_by', 'created_at')
        ascending = request.GET.get('ascending', 'true')
        index_tail = int(limit_n) * 9
        index_head = index_tail - 9
        if ascending != 'true':
            filter_by = '-' + filter_by
        videos = Video.objects.order_by(filter_by)[index_head:index_tail]
        serializer = DisplayVideoSerializer(videos, many=True)
        return Response(serializer.data)


