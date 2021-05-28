from django.urls import path, include
from .views import TutorReviewView, StudentReviewView, GetEditDeleteReviewView

TutorReviewViewAsView = TutorReviewView.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [ 
    path('api/reviews/tutors/<int:pk>', TutorReviewViewAsView, name='create_review'),
    path('api/reviews/students/<int:pk>', StudentReviewView.as_view(), name="student_review"),
    path('api/reviews/<int:pk>', GetEditDeleteReviewView.as_view(), name="handle_review"),
]