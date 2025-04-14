# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('profile/', views.user_profile, name='user_profile'),
#     path('profile/edit/', views.edit_profile, name='edit_profile'),
#     path('profile/delete/', views.delete_account, name='delete_account'),
#     path('', views.home, name='home'),
#     path('create_profile/', views.create_profile, name='create_profile'),
#
# ]
#
#
# user/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.user_profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
