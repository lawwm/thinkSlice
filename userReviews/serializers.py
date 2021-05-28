from rest_framework import serializers
from .models import Review

class AccessReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'tutor_profile': {'read_only' : True },
            'student_profile': {'read_only' : True }
        }
        

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
    def validate(self, data):
        if data['tutor_profile'] == data['student_profile']:
            raise serializers.ValidationError("Cannot rate own profile")
        return data