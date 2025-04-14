# from django.db import models
# from django.contrib.auth.models import User
#
# # Create your models here.
# class UserProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     profile_picture=models.ImageField(upload_to='profile_pics/', blank=True,null=True)
#     birthdate = models.DateField(blank=True, null=True)
#     facebook_profile=models.URLField(blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user.username}'s Profile"

# user/models.py
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    # Phone number validation
    phone_regex = RegexValidator(
        regex=r'^01[0125][0-9]{8}$',
        message="Phone number must be an Egyptian number starting with 010, 011, 012, or 015."
    )
    mobile = models.CharField(validators=[phone_regex], max_length=11, blank=True)

    # Extra fields
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
