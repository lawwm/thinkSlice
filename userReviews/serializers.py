from rest_framework import serializers
from .models import Review
from userProfiles.serializers import ProfileReviewSerializer

class AccessReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'tutor_profile': {'read_only' : True },
            'student_profile': {'read_only' : True }
        }

# When you are reviewed by students
class StudentReviewSerializer(serializers.ModelSerializer):
    creator_details = ProfileReviewSerializer(source='student_profile', read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

# When you are reviewing tutors
class TutorReviewSerializer(serializers.ModelSerializer):
    creator_details = ProfileReviewSerializer(source='tutor_profile', read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        
class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
    def validate(self, data):
        if data['tutor_profile'] == data['student_profile']:
            raise serializers.ValidationError("Cannot rate own profile")
        return data