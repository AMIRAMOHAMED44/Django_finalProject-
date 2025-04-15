# from django.contrib.auth.models import AbstractUser
# from django.core.validators import RegexValidator
# from django.db import models
#
# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=False)
#     phone_regex = RegexValidator(
#         regex=r'^01[0125][0-9]{8}$',
#         message="Phone number must be an Egyptian number starting with 010, 011, 012, or 015."
#     )
#     mobile = models.CharField(validators=[phone_regex], max_length=11, blank=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#
#
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    phone_regex = RegexValidator(
        regex=r'^01[0125][0-9]{8}$',
        message="Phone number must be an Egyptian number starting with 010, 011, 012, or 015."
    )
    mobile = models.CharField(validators=[phone_regex], max_length=11, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='')

    # Add the new optional fields
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"