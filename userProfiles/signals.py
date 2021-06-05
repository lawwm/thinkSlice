from django.contrib.auth.models import User
from userReviews.models import Review
from django.db.models import F
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username)


@receiver(pre_save, sender=Review)
def update_rating_post(sender, instance, **kwargs):
    profile = Profile.objects.get(user=instance.tutor_profile.user)
    try:
        review = Review.objects.get(id=instance.id)
        profile.aggregate_star = (profile.aggregate_star * profile.total_tutor_reviews -
                                  review.star_rating + instance.star_rating) / profile.total_tutor_reviews
    except:
        if (profile.aggregate_star == None):
            profile.aggregate_star = instance.star_rating
        else:
            profile.aggregate_star = (profile.aggregate_star * profile.total_tutor_reviews +
                                      instance.star_rating) / (profile.total_tutor_reviews + 1)
        profile.total_tutor_reviews = F('total_tutor_reviews') + 1
    profile.save()


@ receiver(post_delete, sender=Review)
def update_rating_delete(sender, instance, **kwargs):
    profile = Profile.objects.get(user=instance.tutor_profile.user)
    if (profile.total_tutor_reviews == 1):
        profile.aggregate_star = None
    else:
        profile.aggregate_star = ((profile.aggregate_star * profile.total_tutor_reviews) -
                                  instance.star_rating) / (profile.total_tutor_reviews - 1)
    profile.total_tutor_reviews = F('total_tutor_reviews') - 1
    profile.save()
