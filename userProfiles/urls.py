from django.urls import path, include
from .views import AllProfileView, ProfileView, DetailProfileView, SearchProfileView
from rest_framework import routers


ProfileViewAsView = ProfileView.as_view({
    'get': 'retrieve',
    'post': 'create',
    'patch': 'partial_update',
    'delete': 'destroy'
})

DetailProfileViewAsView = DetailProfileView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'put': 'update'
})

SearchProfileViewAsView = SearchProfileView.as_view({
    'get': 'list',
})


urlpatterns = [ 
    path('api/profiles', AllProfileView.as_view(), name='all_profile'),
    path('api/profiles/<int:pk>', ProfileViewAsView , name='one_profile'),
    path('api/profiles/details/<int:pk>', DetailProfileViewAsView , name='one_detail_profile'),
    path('api/profiles/search', SearchProfileViewAsView, name='search_profile'),
]