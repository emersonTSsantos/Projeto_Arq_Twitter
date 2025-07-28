from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create A User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    date_modified = models.DateTimeField(User, auto_now=True)

    def __str__(self):
        return self.user.username

# Create UserProfile when new User Signs Up
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()
        # Have the user Follow Themselves
        user_profile.follows.set([user_profile])  # Auto-follow
        user_profile.save()

post_save.connect(create_user_profile, sender=User)