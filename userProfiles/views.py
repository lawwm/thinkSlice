from rest_framework import  viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import ProfileGeneralSerializer, ProfileDetailSerializer, ProfilePictureSerializer, ProfileReviewSerializer
from .models import Profile, Similarity
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from accounts.permissions import IsOwnerOrReadOnly
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from django.db import models

#Cache import
from django.core.cache import cache
from appmanager.settings import CACHE_TTL

class AllProfileView(APIView):
    # GET all profiles
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileGeneralSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileView(viewsets.ViewSet):
    parser_classes=[JSONParser, FormParser,MultiPartParser, FileUploadParser]

    #GET one profile(general)
    def retrieve(self, request, *args, **kwargs):
        #Check for cache
        cache_key = request.path
        if (cache.has_key(cache_key)):
            return Response(cache.get(cache_key))

        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        serializer = ProfileGeneralSerializer(profiles, many=False)

        #Set cache value
        cache.set((cache_key), serializer.data, CACHE_TTL)

        return Response(serializer.data)

    # Upload profile picture to S3
    def create(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        serializers = ProfilePictureSerializer(profiles, data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            
            #Delete cache value
            cache_key = request.path
            cache.delete(cache_key)
            return Response(serializers.data)

    # PATCH your own profile (general)
    def partial_update(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        serializer = ProfileGeneralSerializer(profiles, data = request.data, partial=True, many=False)
        if serializer.is_valid(raise_exception=True):
            #Save information
            serializer.save()

            #Set new cache value
            cache_key = request.path
            cache.set((cache_key), serializer.data, CACHE_TTL)

            return Response(serializer.data)
        return Response("Wrong parameters", status=400)

    # DELETE your own profile (general)
    def destroy(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        user_id = profiles.user_id
        user = get_object_or_404(User, pk=user_id)
        user.delete()

        #Delete cache value
        cache_key = request.path
        cache.delete(cache_key)

        return Response("Successfully deleted", status=200)

    # Set permissions for different actions
    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]



class DetailProfileView(viewsets.ViewSet):
    # GET one profile (detail)
    def retrieve(self, request, *args, **kwargs):
        #Check for cache
        cache_key = request.path
        if (cache.has_key(cache_key)):
            return Response(cache.get(cache_key))

        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        serializer = ProfileDetailSerializer(profiles, many=False)
        
        #Set cache value
        cache.set((cache_key), serializer.data, CACHE_TTL)

        return Response(serializer.data)

    # PATCH your own profile (detail)
    def partial_update(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        serializer = ProfileDetailSerializer(profiles, data = request.data, partial=True, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            #Set new cache value
            cache_key = request.path
            cache.set((cache_key), serializer.data,  CACHE_TTL)

            return Response(serializer.data)
        return Response("Wrong parameters", status=400)

    # PUT a refreshed detail page
    def update(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        data = {
                    "tutor_whatsapp": None,
                    "tutor_telegram": None,
                    "duration_classes": [0, 0],
                    "subjects": None,
                    "qualifications": ""
                }
        serializer = ProfileDetailSerializer(profiles, data=data, partial=True, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            #Set new cache value
            cache_key = request.path
            cache.set((cache_key), serializer.data, CACHE_TTL)

            return Response(serializer.data)
        return Response("Wrong parameters", status=400)


    # Set permissions for different actions
    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

class SearchProfileView(viewsets.ViewSet):
    def list(self, request):
        search_name = request.GET.get('name', None)
        if search_name == None:
            cache.clear()
            return Response('Cache cleared', status=400)
        profiles = Profile.objects.annotate(
            match=Similarity("username", models.Value(search_name)), 
        ).filter(match__gt=0.20)
        serializers = ProfileReviewSerializer(profiles, many=True)
        cache.clear()
        return Response(serializers.data)
