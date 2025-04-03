from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture=models.ImageField(upload_to='profile_pics/', blank=True,null=True)
    birthdate = models.DateField(blank=True, null=True)
    facebook_profile=models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

