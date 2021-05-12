from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def save_create_profile(sender, instance, created, **kwargs):
    if created:
        print(sender)
        print(instance)
        print(created)
        #create coordinate profile of user
        Profile.objects.create(user=instance)