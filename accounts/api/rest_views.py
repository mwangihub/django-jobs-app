import uuid
import six
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import decorators

from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode as encode, urlsafe_base64_decode as decode
from core.methods import send_mass_mail
from . import serializers

User = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    '''
    overriding  _make_hash_value
    '''

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


_token_generator = TokenGenerator()


class UsersViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser, ]


class EmployeeSignUpViewSet(viewsets.ViewSet):
    """
    create a new Employee User and sends confirmation link through email.
    """
    queryset = User.objects.all()
    '''
    if the viewset does not include a queryset attribute then 
    you must set basename when registering the viewset.
    '''
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            user.first_name = serializer.validated_data['first_name']
            user.second_name = serializer.validated_data['second_name']
            user.employee = True
            to_email = serializer.validated_data['email']

            message = {
                'subject': 'Activate Your Account',
                'recipients': [to_email, ],
                'template': 'api/registration/api_acc_active_email.html',
                'context': {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': encode(force_bytes(user.pk)),
                    'token': _token_generator.make_token(user),
                }
            }
            send_mass_mail([message])
            user.save()
            messages.success(
                request, f'A confirmation link has been sent to {to_email}. Check your email to complete registration.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['GET', ])
def confirm_account(request, uidb64, token):
    if request.method == 'GET':
        try:
            uid = force_text(decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            messages.warning(
                request, 'The confirmation link was invalid, possibly because it has already been used.')
            return Response({'redirect': "redirect user to register page"}, status=status.HTTP_400_BAD_REQUEST)
        if user is not None and _token_generator.check_token(user, token):
            user.active = True
            user.save()
            login(request, user)
            messages.success(
                request, f'Hi {user}, Your account have been confirmed.')
            return Response({'redirect': "redirect user to the appropiate page"}, status=status.HTTP_200_OK
                            )
        else:
            messages.warning(
                request, 'The confirmation link was invalid, possibly because it has already been used.')
            return Response({'redirect': "redirect user to register page"}, status=status.HTTP_400_BAD_REQUEST)
