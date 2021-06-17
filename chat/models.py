from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from userProfiles.models import Profile

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatRoom(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="owner")
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="recipient")
    messages = models.ManyToManyField(Message, blank=True)
