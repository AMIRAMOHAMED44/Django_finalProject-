# accounts/urls.py
from django.urls import path
from .views import SignUpView, CustomLoginView ,activate_account, activation_sent , resend_activation_email
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activation-sent/', activation_sent, name='activation_sent'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('resend/', resend_activation_email, name='resend_activation'),
   
]
