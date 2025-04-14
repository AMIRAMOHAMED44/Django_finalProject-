# from django.shortcuts import render, redirect
# from .forms import RegistrationForm, UserProfileForm, CustomUserChangeForm
# from .models import UserProfile
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import update_session_auth_hash
#
#
# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             UserProfile.objects.create(user=user)
#             login(request, user)
#             return redirect('user_profile')
#     else:
#         form = RegistrationForm()
#     return render(request, 'user/register.html', {'form': form})
#
#
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'user/login.html', {'form': form})
#
#
# @login_required
# def create_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             # Save the form data to create the profile for the user
#             user_profile = form.save(commit=False)
#             user_profile.user = request.user  # Link the profile to the current user
#             user_profile.save()
#             return redirect('user_profile')  # After creating the profile, go to the profile page
#     else:
#         form = UserProfileForm()
#
#     return render(request, 'user/create_profile.html', {'form': form})
#
#
# @login_required
# def user_profile(request):
#     try:
#         profile = UserProfile.objects.get(user=request.user)
#         return render(request, 'user/profile.html', {'profile': profile})
#     except UserProfile.DoesNotExist:
#         return redirect('create_profile')
# @login_required
# def edit_profile(request):
#     user = request.user
#
#     profile, created = UserProfile.objects.get_or_create(user=user)
#
#     if request.method == 'POST':
#         user_form = CustomUserChangeForm(request.POST, instance=user)
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('user_profile')
#     else:
#         user_form = CustomUserChangeForm(instance=user)
#         profile_form = UserProfileForm(instance=profile)
#
#     return render(request, 'user/edit_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#     })
#
# @login_required
# def delete_account(request):
#     if request.method == 'POST':
#         password = request.POST.get('password')  # Get password from the POST request
#         user = request.user
#
#         # Verify the entered password
#         if user.check_password(password):
#             logout(request)
#             user.delete()  # Delete the user account
#             return redirect('home') # Redirect to a goodbye page or home page
#         else:
#             # If password is incorrect, return an error message to the user
#             return render(request, 'user/delete_account.html', {'error': 'Incorrect password'})
#
#     return render(request, 'user/delete_account.html')
#
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)  # Keeps the user logged in after password change
#             return redirect('password_change_done')  # Redirect to a success page
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {'form': form})
#
# def home(request):
#     return render(request, 'user/home.html')  # Ensure this path is correct


# user/views.py
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CustomUserChangeForm, AuthenticationFormCustom
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})


# Profile view
# @login_required
# def user_profile(request):
#     user = request.user
    # user_projects = Project.objects.filter(owner=user)  # If you have a Project model
    # user_donations = Donation.objects.filter(user=user)  # If you have a Donation model

    # context = {
    #     'user': user,
    #     'projects': user_projects,
    #     'donations': user_donations,
    # }
    # return render(request, 'user/profile.html', context)

@login_required
def user_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'user/profile.html', context)
# Edit Profile view

def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'user/edit_profile.html', {'form': form})


# Login view (email login)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationFormCustom(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')  # Redirect to profile after login
    else:
        form = AuthenticationFormCustom()
    return render(request, 'user/login.html', {'form': form})


# Password Change view
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps the user logged in after password change
            return redirect('password_change_done')  # Redirect to a success page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home or login page after logout


# Account deletion (password confirmation required)
@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST['password']
        if request.user.check_password(password):
            request.user.delete()
            messages.success(request, "Account deleted successfully.")
            return redirect('home')
        else:
            messages.error(request, "Incorrect password.")
    return render(request, 'user/delete_account.html')


def home(request):
    return render(request, 'user/home.html')
