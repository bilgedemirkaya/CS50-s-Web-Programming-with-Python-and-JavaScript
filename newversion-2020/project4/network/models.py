from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', unique=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_image", blank = True)
    description = models.CharField(blank=True,max_length=100)
    city = models.CharField(max_length=64)
    firstname = models.CharField(max_length=64)

class UserPost(models.Model):
    owner = models.ForeignKey(UserProfile,related_name='owner',on_delete=models.CASCADE)
    post = models.CharField(max_length=150)
    likes = models.ManyToManyField(User,related_name='likers')
    timestamp = models.DateTimeField(auto_now=True)