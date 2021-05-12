from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models import CASCADE


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    bio = models.TextField(default="no bio yet... update required")
    avatar = models.ImageField(upload_to='avatars',default='no_picture.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
