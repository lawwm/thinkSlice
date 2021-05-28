from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from userProfiles.models import Profile
from userReviews.models import Review
from .serializers import CreateReviewSerializer, AccessReviewSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import IsReviewerOrReadOnly
# Create your views here.

# Create review/ list all tutor's reviews
class TutorReviewView(viewsets.ViewSet):
    # serializer_class = CreateReviewSerializer

    def create(self, request, *args, **kwargs):
        # Get tutor and student profile
        request.data['tutor_profile'] = get_object_or_404(Profile, user=kwargs['pk']).id
        request.data['student_profile'] = get_object_or_404(Profile, user=request.user.id).id

        # Check that student hasn't already reviewed the teacher
        check_existing = Review.objects.filter(tutor_profile=request.data['tutor_profile'], 
            student_profile=request.data['student_profile'])
        if check_existing.exists():
            return Response("You've already reviewed this particular user", status=status.HTTP_400_BAD_REQUEST)

        # Use serializer validation
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        profile_id = get_object_or_404(Profile, user=kwargs['pk']).id
        reviews = Review.objects.filter(tutor_profile=profile_id)
        serializer = AccessReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def get_permissions(self):    
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# Get all reviews based on student
class StudentReviewView(generics.ListAPIView):
    serializer_class = AccessReviewSerializer
    def get_queryset(self):
        student_profile = get_object_or_404(Profile, user=self.kwargs['pk']).id
        return Review.objects.filter(student_profile=student_profile)

# Delete all reviews(later)


# Get/Edit/Delete one review
class GetEditDeleteReviewView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = AccessReviewSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Once patch request accesses endpoint, edited becomes true
        request.data["edited"] = True
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        review = get_object_or_404(Review, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, review)
        return review

    def get_permissions(self):
        
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsReviewerOrReadOnly]
        return [permission() for permission in permission_classes]

