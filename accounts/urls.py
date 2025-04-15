# # accounts/urls.py
# from django.urls import path
# from .views import SignUpView, CustomLoginView ,activate_account, activation_sent , resend_activation_email
# from django.contrib.auth.views import LogoutView
#
# urlpatterns = [
#     path('signup/', SignUpView.as_view(), name='signup'),
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('activation-sent/', activation_sent, name='activation_sent'),
#     path('activate/<uidb64>/<token>/', activate_account, name='activate'),
#     path('resend/', resend_activation_email, name='resend_activation'),
#
# ]
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    SignUpView,
    CustomLoginView,
    activate_account,
    activation_sent,
    resend_activation_email,
    ProfileView,
    EditProfileView,
    delete_account_view
)

urlpatterns = [
    # Authentication URLs
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Account Activation URLs
    path('activation-sent/', activation_sent, name='activation_sent'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('resend/', resend_activation_email, name='resend_activation'),

    # Profile URLs
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/delete/', delete_account_view, name='delete_account'),
]