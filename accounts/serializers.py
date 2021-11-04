from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import User

User = get_user_model()


# SERIALIZERS
class ThreadSerializer(serializers.ModelSerializer):
    #    class Meta:
    #       model = ConnectionHistory
    #       fileds ='__all__'

    pass


class UserSerializer(serializers.ModelSerializer):
    get_full_name = serializers.CharField()

    class Meta:
        model = User
        fields = "__all__"


class ConnectionHistorySerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=True)
    # class Meta:
    #     model = ConnectionHistory
    #     fields = ('id', 'user', 'first_login', 'last_echo', 'logged')
    pass
