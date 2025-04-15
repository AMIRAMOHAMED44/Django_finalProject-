# # accounts/forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser
# from django.contrib.auth.forms import AuthenticationForm
#
#
# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email', 'mobile', 'profile_picture', 'password1', 'password2']
#
# class EmailLoginForm(AuthenticationForm):
#     username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'mobile', 'profile_picture', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class UserProfileForm(UserChangeForm):
    password = None  # Remove password field from the form

    birthdate = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    facebook_profile = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'}),
    )
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'mobile',
            'profile_picture',
            'birthdate',
            'facebook_profile',
            'country'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        label=_("Confirm your password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise ValidationError(_("Incorrect password"))
        return password


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
    )