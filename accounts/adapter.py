'''
    Overidding adapters to change core behaviour of redirects and how user will be saved.
    User attr can be also be changed in signals in signals.py
        allauth.socialaccount.adapter.DefaultSocialAccountAdapter
        allauth.account.adapter.DefaultAccountAdapter
'''
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse

class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        '''
        If user requests login page but is already authenticated is redirected to home page
        '''
        url = reverse("innovesthome:innovest-home")
        return url

    def get_signup_redirect_url(self, request):
        url = reverse("user_urls:choose-user")
        return url

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        assert request.user.is_authenticated
        url = reverse("profile")
        return url

