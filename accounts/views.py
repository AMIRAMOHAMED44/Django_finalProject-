# accounts/views.py
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from .forms import SignUpForm, EmailLoginForm
from .models import CustomUser
#>>>>>>>>>>>
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render
#.......
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # deactivate the user until email is verified
        user.save()

        # prepare activation email
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

