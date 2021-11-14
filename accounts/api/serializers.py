from ..models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'second_name',
            'slug',
            'active',
            'staff',
            'admin',
            'buyer',
            'employee',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['email','first_name','second_name','password','password2']
        extra_kwargs = {
                'first_name': {'required': True},
                'second_name': {'required': True}
            }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
