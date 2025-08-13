from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create meep model
class Meep(models.Model):
    user = models.ForeignKey(User, related_name='meeps', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='meep_like', blank=True)

    # Keep track or count of likes
    @property
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        local_time = timezone.localtime(self.created_at)
        return (
            f"{self.user}" 
            f"({self.created_at:%d-%m-%Y {local_time:%H:%M}}): "
            f"{self.body}..."
        )

# Create A User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
    
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