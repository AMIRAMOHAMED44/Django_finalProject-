# # accounts/views.py
# from django.views.generic.edit import CreateView
# from django.contrib.auth.views import LoginView
# from django.urls import reverse_lazy
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.shortcuts import redirect
# from django.contrib import messages
# from .forms import SignUpForm, EmailLoginForm
# from .models import CustomUser
# #>>>>>>>>>>>
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.http import HttpResponse
# from django.shortcuts import render
# #.......
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
#
#
# class SignUpView(CreateView):
#     model = CustomUser
#     form_class = SignUpForm
#     template_name = 'accounts/signup.html'
#     success_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         # If username is not provided, set it to user's email to ensure uniqueness.
#         if not user.username:
#             user.username = user.email
#         user.is_active = False  # deactivate the user until email is verified
#         user.save()
#
#         # Prepare activation email
#         current_site = get_current_site(self.request)
#         subject = 'Activate your account'
#         message = render_to_string('accounts/account_activation_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': default_token_generator.make_token(user),
#         })
#
#         user.email_user(subject, message)
#         messages.success(self.request, 'Check your email to activate your account.')
#         return redirect('login')
#
#
# def activate_account(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = get_user_model().objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None
#
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('Your account has been activated. You can now <a href="/accounts/login/">login</a>.')
#     else:
#         return render(request, 'accounts/activation_invalid.html')
#
#
#
# def activation_sent(request):
#     return render(request, 'accounts/activation_sent.html')
#
#
#
# @login_required
# def resend_activation_email(request):
#     user = request.user
#     if user.is_active:
#         messages.info(request, 'Your account is already active.')
#         return redirect('login')
#
#     current_site = get_current_site(request)
#     subject = 'Resend Activation Link'
#     message = render_to_string('accounts/account_activation_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': default_token_generator.make_token(user),
#     })
#
#     user.email_user(subject, message)
#     messages.success(request, 'A new activation link has been sent to your email.')
#     return redirect('activation_sent')
#
# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'
#     authentication_form = EmailLoginForm
#
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, EmailLoginForm, UserProfileForm, DeleteAccountForm
from .models import CustomUser
from projects.models import Project, Donation  # Adjust import based on your project structure


class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        if not user.username:
            user.username = user.email
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate your account'
        message = render_to_string('accounts/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        user.email_user(subject, message)
        messages.success(self.request, 'Check your email to activate your account.')
        return redirect('login')


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Your account has been activated. You can now <a href="/accounts/login/">login</a>.')
    else:
        return render(request, 'accounts/activation_invalid.html')


def activation_sent(request):
    return render(request, 'accounts/activation_sent.html')


@login_required
def resend_activation_email(request):
    user = request.user
    if user.is_active:
        messages.info(request, 'Your account is already active.')
        return redirect('login')

    current_site = get_current_site(request)
    subject = 'Resend Activation Link'
    message = render_to_string('accounts/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    user.email_user(subject, message)
    messages.success(request, 'A new activation link has been sent to your email.')
    return redirect('activation_sent')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailLoginForm


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['projects'] = Project.objects.filter(creator=user)
        context['donations'] = Donation.objects.filter(user=user)
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.user, request.POST)
        if form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('home')
    else:
        form = DeleteAccountForm(request.user)

    return render(request, 'accounts/confirm_delete.html', {'form': form})
