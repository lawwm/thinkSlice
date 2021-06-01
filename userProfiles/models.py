from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.db.models.fields import NullBooleanField
#from django.db.models.lookups import IsNull

# Create your models here.


class Profile(models.Model):
    # Default profile information
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        editable=False
    )
    profile_pic = models.ImageField(
        upload_to='user-images/', default='user-images/download.jpg')
    username = models.CharField(max_length=255)
    user_bio = models.TextField(
        blank=True, default='Hi, welcome to my profile!')
    is_tutor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    # If is_tutor is true
    tutor_contact = models.CharField(blank=True, max_length=255)
    tutor_whatsapp = models.IntegerField(blank=True, null=True)
    tutor_telegram = models.CharField(max_length=255, blank=True, null=True)
    aggregate_star = models.FloatField(blank=True, null=True)
    duration_classes = ArrayField(models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]), blank=True, null=True)
    subjects = ArrayField(models.CharField(
        max_length=55), blank=True, null=True)
    total_tutor_reviews = models.IntegerField(default=0)
    qualifications = models.CharField(blank=True, max_length=255)
    #schedule = models.ArrayField()

    # If is_student is true
    #total_student_reviews = models.IntegerField(default=0)

    # def clear_tutor(self):
    #     self.tutor_contact = ''
    #     self.qualifications = ''
    #     self.aggregate_star = None
    #     self.duration_classes = []
    #     self.subjects = []