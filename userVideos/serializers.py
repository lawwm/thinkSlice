from django.db.models.fields import IntegerField
from mux_python.models.asset import Asset
from rest_framework import serializers
from .models import Video, VideoComments, VideoLikes

class UploadResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    status = serializers.CharField()
    url = serializers.URLField()
    timeout = IntegerField()

class CreateVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class ProfileVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['asset_id', 'playback_id', 'duration','created_at']    

class DisplayVideoSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # profile_pic = serializers.CharField()

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['asset_id', 'playback_id', 'duration','created_at', 'creator_profile']
        depth = 1

class DisplayLikedVideoSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # profile_pic = serializers.CharField()
    hasUserLiked = serializers.BooleanField()
    
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['asset_id', 'playback_id', 'duration','created_at', 'creator_profile']
        depth = 1


class LikeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLikes
        fields = '__all__'

class LikedVideoDisplaySerializer(serializers.ModelSerializer):
    videoDetails = DisplayVideoSerializer(source='liked_video', read_only=True)
    class Meta:
        model = VideoLikes
        fields = '__all__'

class VideoCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user_commenting.username")
    profilePic = serializers.URLField(read_only=True, source="user_commenting.profile_pic")
    userId = serializers.IntegerField(read_only=True, source="user_commenting.user.id")
    class Meta:
        model = VideoComments
        fields = '__all__'

class AccessCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user_commenting.username")
    profilePic = serializers.URLField(read_only=True, source="user_commenting.profile_pic")
    userId = serializers.IntegerField(read_only=True, source="user_commenting.user.id")
    class Meta:
        model = VideoComments
        fields = '__all__'
        extra_kwargs = {
            'commented_video': {'read_only' : True },
            'user_commenting': {'read_only' : True }
        }
        