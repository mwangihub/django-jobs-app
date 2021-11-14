'''
Seperation of concerns. since we want the accounts app to handle CRUD for users
'''

import six
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode as encode, urlsafe_base64_decode as decode
from django.views.generic import CreateView, FormView, TemplateView
from . import forms


User = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    '''
    overriding  _make_hash_value
    '''
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)

        
_token_generator = TokenGenerator()


def send_mail_method(user=None, domain=None, subject=None, email=None):
    message = render_to_string('registration/acc_active_email.html', {
        'user': user,
        'domain': domain,
        'uid': encode(force_bytes(user.pk)),
        'token': _token_generator.make_token(user),
    })
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email,])


class UserLoginView(LoginView):
    authentication_form = forms.CustomAuthForm
    template_name = "register/login.html"

    def get_success_url(self):
        if self.request.user.is_employee:
            return reverse_lazy('jobs:job-posts')
        return reverse_lazy('innovesthome:innovest-home')

class UserLogoutView(LogoutView):
    next_page ='innovesthome:innovest-home'

class SignUpViewMain(TemplateView):
    template_name = 'registration/signup_main.html'


class SignUpView(CreateView):
    form_class = forms.RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('/')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False  # Deactivate account till it is confirmed
            user.staff = False
            user.save()

            #########################################################
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                #  'uid': encode(force_bytes(user.pk)).decode(),
                'uid': encode(force_bytes(user.pk)),
                'token': _token_generator.make_token(user),
                # 'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
            messages.success(
                request, f'A confirmation link has been sent to {to_email}. Check your email to complete registration.')
            ########################################################

            # return redirect('user_urls:user_login')
            return redirect('user_urls:user_login')
        else:
            messages.error(request, form.errors)
            return render(request, self.template_name, {'form': form})


class EmployeeSignUpView(CreateView):
    model = User
    form_class = forms.EmployeeSignUpForm
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        kwargs['type'] = 'employee'
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.staff = False
            domain = get_current_site(request).domain
            subject = 'Activate Your Account'
            to_email = form.cleaned_data.get('email')
            send_mail_method(user=user, domain=domain,
                             subject=subject, email=to_email)
           
            user.save()
            messages.success(
                request, f'A confirmation link has been sent to {to_email}. Check your email to complete registration.')
            return redirect('user_urls:register-employee')
        else:
            messages.error(request, form.errors)
            return render(request, self.template_name, {'form': form})


class CustomerSignUpView(CreateView):
    model = User
    form_class = forms.CustomerSignUpForm
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        kwargs['type'] = 'customer'
        print(kwargs)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.staff = False
            user.save()
            domain = get_current_site(request).domain
            subject = 'Activate Your Account'
            to_email = form.cleaned_data.get('email')
            send_mail_method(user=user, domain=domain,
                             subject=subject, email=to_email)

            messages.success(
                request, f'A confirmation link has been sent to {to_email}. Check your email to complete registration.')
            return redirect('user_urls:register-cutomer')
        else:
            messages.error(request, form.errors)
            return render(request, self.template_name, {'form': form})


def confirm_account(request, uidb64, token):
    try:
        uid = force_text(decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print(TypeError, ValueError, OverflowError, User.DoesNotExist)
        print("TypeError, ValueError, OverflowError, User.DoesNotExist")
    if user is not None and _token_generator.check_token(user, token):
        user.active = True
        user.staff = False
        user.save()
        login(request, user)
        messages.success(
            request, f'Hi {user}, Your account have been confirmed.')
        if user.is_buyer:
            return redirect('affiliate:market-place')
        if user.is_employee:
            return redirect('jobs:job-posts')
    else:
        messages.warning(
            request, 'The confirmation link was invalid, possibly because it has already been used.')
        return redirect('user_urls:register')


class ResetPasswordRequestView(FormView):
    template_name = "registration/reset-password.html"
    success_url = '/user/accounts/reset-password/'
    form_class = forms.PasswordResetRequestForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            associated_users = User.objects.filter(
                email__iexact=data, active=True)
            if associated_users.exists():
                for user in associated_users:
                    #########################################################
                    user.active = False
                    if user.staff:
                        user.staff = False
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Reset your Password'
                    message = render_to_string('registration/password_reset_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                    send_mail(subject, message,
                              settings.DEFAULT_FROM_EMAIL, [to_email])

                    messages.success(request, 'We will be sending email with a link to reset your password')
                    ########################################################

                result = self.form_valid(form)
                messages.success(request,
                                 f'An email has been sent to {data}. Please check its inbox to continue reseting password.')
                return result
            result = self.form_invalid(form)
            messages.error(
                request, 'No user is associated with this email address. Or did you request \
                    for password reset multiple times? Check your email or if you cant find the link, contact admin.')
            return result
        messages.error(
            request, 'Invalid Email. Check your email and try again.')
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "registration/password_reset_confirm.html"
    success_url = '/'
    form_class = forms.SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset with success.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset is unsuccessful.')
                return self.form_invalid(form)
        else:
          
            messages.error(
                request, 'Password reset  link is no longer valid.')
            # return self.form_invalid(form)
            return redirect('/')
            


