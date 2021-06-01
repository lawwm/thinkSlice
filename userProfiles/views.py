from django.shortcuts import render
from rest_framework import generics, serializers, permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import ProfileGeneralSerializer, ProfileDetailSerializer, ProfilePictureSerializer
from .models import Profile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from accounts.permissions import IsOwnerOrReadOnly
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser


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
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        serializer = ProfileGeneralSerializer(profiles, many=False)
        return Response(serializer.data)

    # Upload profile picture to S3
    def create(self, request, *args, **kwargs):
        print(request.data['profile_pic'])
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        print("hello there")
        serializers = ProfilePictureSerializer(profiles, data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data)

    # PATCH your own profile (general)
    def partial_update(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        serializer = ProfileGeneralSerializer(profiles, data = request.data, partial=True, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response("Wrong parameters", status=400)

    # DELETE your own profile (general)
    def destroy(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        user_id = profiles.user_id
        user = get_object_or_404(User, pk=user_id)
        user.delete()
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
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        serializer = ProfileDetailSerializer(profiles, many=False)
        return Response(serializer.data)

    # PATCH your own profile (detail)
    def partial_update(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        serializer = ProfileDetailSerializer(profiles, data = request.data, partial=True, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response("Wrong parameters", status=400)

    # PUT a refreshed detail page
    def update(self, request, *args, **kwargs):
        profiles = get_object_or_404(Profile, user=kwargs['pk'])
        self.check_object_permissions(self.request, profiles)
        data = {
                    "tutor_contact": "",
                    "aggregate_star": None,
                    "duration_classes": None,
                    "subjects": None,
                    "qualifications": ""
                }
        serializer = ProfileDetailSerializer(profiles, data=data, partial=True, many=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response("Wrong parameters", status=400)


    # Set permissions for different actions
    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
