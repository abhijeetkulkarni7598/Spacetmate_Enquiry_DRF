from rest_framework import serializers
from app.models import *
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
UserAccount = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model=UserAccount
        fields=('__all__')


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserAccount
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields="__all__"


from django.contrib.auth.password_validation import validate_password

from djoser.serializers import UserCreateSerializer
from app.models import UserAccount

class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = '__all__'


# serializers.py

from rest_framework import serializers
from app.models import UserAccount  # Replace with your actual model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('__all__')  # Add other fields as needed
