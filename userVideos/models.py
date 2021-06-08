from django.db import models
from userProfiles.models import Profile
from django.contrib.auth.models import User

# Create your models here.
class Video(models.Model):
    # Create from request.data
    video_title = models.CharField(max_length=70)
    video_description = models.CharField(max_length=400)
    creator_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="creator_profile")
    subject = models.CharField(max_length = 100)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    num_of_comments = models.IntegerField(default=0)

    # Found within assets object attributes
    asset_id = models.CharField(max_length = 200)
    playback_id = models.CharField(max_length = 200)
    duration = models.FloatField()
    policy = models.CharField(max_length = 100)
    created_at = models.IntegerField()

    def likeCount(self):
        return VideoLikes.objects.filter(video=self).count()

    def commentCount(self):
        return VideoComments.objects.filter(video=self).count()
    
class VideoLikes(models.Model):
    liked_video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="liked_video")
    user_liking = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_liking")

class VideoComments(models.Model):
    commented_video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="commented_video")
    user_commenting = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_commenting")
    comment_text = models.TextField()
    date_comment = models.DateField(auto_now_add=True)
    date_comment_edited = models.DateField(auto_now=True)
    edited = models.BooleanField(default=False)
    has_replies = models.BooleanField(default=False)
    parent_comment = models.ForeignKey("VideoComments", on_delete=models.CASCADE, blank=True, null=True)

