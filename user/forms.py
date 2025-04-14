# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
# from django.contrib.auth.models import User
# from .models import UserProfile
#
# class RegistrationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     phone_number = forms.CharField(max_length=15, required=True)
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']
#
#
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['phone_number', 'profile_picture', 'birthdate', 'facebook_profile', 'country']
#
# class PasswordConfirmationForm(forms.Form):
#     password = forms.CharField(widget=forms.PasswordInput)
#
# class AuthenticationFormCustom(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password']
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']

# user/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


# Registration Form for CustomUser
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=11, required=True)  # Egyptian phone numbers
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser  # Now it uses CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'profile_picture', 'password1', 'password2']


# Change Form for CustomUser (Profile)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'profile_picture', 'birthdate', 'facebook_profile', 'country']


# Authentication form for login (email-based login)
class AuthenticationFormCustom(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autofocus': True}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
