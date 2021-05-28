from django.db.models.fields import IntegerField
from mux_python.models.asset import Asset
from rest_framework import serializers
from .models import Video

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
        read_only_fields = ['asset_id', 'playback_id', 'duaration','created_at']    

class DisplayVideoSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # profile_pic = serializers.CharField()

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['asset_id', 'playback_id', 'duaration','created_at', 'creator_profile']
        depth = 1