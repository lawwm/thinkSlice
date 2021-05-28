from django.db import models
from userProfiles.models import Profile

# Create your models here.
class Review(models.Model):
    
    star_rating = models.FloatField()
    review_title = models.CharField(max_length=150)
    review_essay = models.TextField()
    date_review = models.DateField(auto_now_add=True)
    date_review_editted = models.DateField(auto_now=True)

    edited = models.BooleanField(default=False)
    tutor_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tutor_profile")
    student_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="student_profile")

