from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from userProfiles.models import Profile
from userReviews.models import Review
from .serializers import CreateReviewSerializer, AccessReviewSerializer, StudentReviewSerializer, TutorReviewSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import IsReviewerOrReadOnly
# Create your views here.

#Cache imports
from django.core.cache import cache
from appmanager.settings import CACHE_TTL
# Create review/ list all tutor's reviews


class TutorReviewView(viewsets.ViewSet):
    # serializer_class = CreateReviewSerializer

    def create(self, request, *args, **kwargs):
        # Get tutor and student profile
        profile = get_object_or_404(Profile, user=kwargs['pk'])
        request.data['tutor_profile'] = profile.id
        request.data['student_profile'] = get_object_or_404(
            Profile, user=request.user.id).id

        # Check that student hasn't already reviewed the teacher
        check_existing = Review.objects.filter(tutor_profile=request.data['tutor_profile'],
                                               student_profile=request.data['student_profile'])
        if check_existing.exists():
            return Response("You've already reviewed this particular user", status=status.HTTP_400_BAD_REQUEST)

        # Use serializer validation
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if (profile.aggregate_star == None):
            profile.aggregate_star = request.data['star_rating']
        else:
            profile.aggregate_star = (profile.aggregate_star * profile.total_tutor_reviews +
                                      request.data['star_rating'])/(profile.total_tutor_reviews + 1)
        profile.total_tutor_reviews = profile.total_tutor_reviews + 1
        profile.save()

        #Delete existing caches
        tutor_cache_key = "/api/reviews/tutors/" + str(kwargs['pk'])
        student_cache_key = "/api/reviews/students/" + str(request.user.id)
        cache.delete(tutor_cache_key)
        cache.delete(student_cache_key)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        #Check for cache
        cache_key = request.path
        if (cache.has_key(cache_key)):
            return Response(cache.get(cache_key))

        profile_id = get_object_or_404(Profile, user=kwargs['pk']).id
        reviews = Review.objects.select_related('student_profile').filter(tutor_profile=profile_id)
        serializer = StudentReviewSerializer(reviews, many=True)

        #Set cache value
        cache.set((cache_key), serializer.data, CACHE_TTL)

        return Response(serializer.data)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# Get all reviews based on student
class StudentReviewView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        #Check for cache
        cache_key = request.path
        if (cache.has_key(cache_key)):
            return Response(cache.get(cache_key))

        student_profile = get_object_or_404(Profile, user=self.kwargs['pk']).id
        reviews = Review.objects.select_related('tutor_profile').filter(student_profile=student_profile)
        serializer = TutorReviewSerializer(reviews, many=True)

        #Set cache value
        cache.set((cache_key), serializer.data, CACHE_TTL)

        return Response(serializer.data)


# Delete all reviews(later)


# Get/Edit/Delete one review
class GetEditDeleteReviewView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = AccessReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Once patch request accesses endpoint, edited becomes true
        request.data["edited"] = True
        old_review = Review.objects.get(id=kwargs['pk'])
        profile = get_object_or_404(Profile, id=old_review.tutor_profile.id)
        if (type(request.data['star_rating']) == str):
            request.data['star_rating'] = float(request.data['star_rating'])
        profile.aggregate_star = (profile.aggregate_star * profile.total_tutor_reviews - old_review.star_rating +
                                  request.data['star_rating'])/profile.total_tutor_reviews
        profile.save()

        #Delete existing caches
        tutor_cache_key = "/api/reviews/tutors/" + str(profile.user_id)
        student_cache_key = "/api/reviews/students/" + str(request.user.id)
        cache.delete(tutor_cache_key)
        cache.delete(student_cache_key)

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        review = Review.objects.get(id=kwargs['pk'])
        student_profile = get_object_or_404(Profile, id=review.student_profile.id)
        if (student_profile.user_id != request.user.id):
            return Response("You do not have access to this review", status=403)
        profile = get_object_or_404(Profile, id=review.tutor_profile.id)
        profile.total_tutor_reviews = profile.total_tutor_reviews - 1
        if (profile.total_tutor_reviews == 0):
            profile.aggregate_star = None
        else:
            profile.aggregate_star = (profile.aggregate_star * (profile.total_tutor_reviews + 1) -
                                        review.star_rating)/profile.total_tutor_reviews
        profile.save()

        #Delete existing caches
        tutor_cache_key = "/api/reviews/tutors/" + str(profile.user_id)
        student_cache_key = "/api/reviews/students/" + str(request.user.id)
        cache.delete(tutor_cache_key)
        cache.delete(student_cache_key)

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
