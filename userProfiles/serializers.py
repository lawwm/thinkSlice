from rest_framework import serializers
from .models import Profile
from userVideos.serializers import ProfileVideoSerializer

# General Profile Serializers
class ProfileGeneralSerializer(serializers.ModelSerializer):
    video = ProfileVideoSerializer(many=True, read_only=True, source='creator_profile')

    class Meta:
        model = Profile
        fields = ['id', 'profile_pic', 'username', 'user_bio', 'is_tutor', "is_student", 'user', 'video']
        extra_kwargs = {'user' : {'read_only': True}, 'profile_pic' : {'read_only': True} }

class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(        
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Profile
        fields = ['profile_pic']

# Detailed Profile Serializers
class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['tutor_whatsapp', 'tutor_telegram', 'aggregate_star', 'location', 'duration_classes', 
        'subjects', 'total_tutor_reviews', 'qualifications']
        extra_kwargs = {'user' : {'read_only': True}, 'aggregate_star': {'read_only': True} }

# Serializer for getting profile information within review
class ProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'username', 'user']
        extra_kwargs = {'username' : {'read_only': True}, 'profile_pic' : {'read_only': True} }