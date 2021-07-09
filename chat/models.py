from userProfiles.models import Profile
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatRoom(models.Model):
    messages = models.ManyToManyField(Message, blank=True)

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    recipientProfile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="recipientProfile")
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="chatroom")
    hidden = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    last_message_count = models.IntegerField(default=0)
    new_message_count = models.IntegerField(default=0)
