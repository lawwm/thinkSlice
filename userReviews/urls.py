from django.urls import path, include
from .views import TutorReviewView, StudentReviewView, GetEditDeleteReviewView

TutorReviewViewAsView = TutorReviewView.as_view({
    'get': 'list',
    'post': 'create',
})

StudentReviewViewAsView = StudentReviewView.as_view({
    'get': 'list',
})

urlpatterns = [ 
    path('api/reviews/tutors/<int:pk>', TutorReviewViewAsView, name='create_review'),
    path('api/reviews/students/<int:pk>', StudentReviewViewAsView, name="student_review"),
    path('api/reviews/<int:pk>', GetEditDeleteReviewView.as_view(), name="handle_review"),
]