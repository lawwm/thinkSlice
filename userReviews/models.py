from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from userProfiles.models import Profile

# Create your models here.


class Review(models.Model):

    star_rating = models.FloatField()
    review_title = models.CharField(max_length=150)
    review_subject = ArrayField(models.CharField(
        max_length=55), blank=True, null=False, default=list)
    review_essay = models.TextField()
    date_review = models.DateField(auto_now_add=True)
    date_review_edited = models.DateField(auto_now=True)

    edited = models.BooleanField(default=False)
    tutor_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="tutor_profile")
    student_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="student_profile")
