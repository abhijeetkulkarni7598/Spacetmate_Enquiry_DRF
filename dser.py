from rest_framework import serializers
from app.models import *
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model=User
        fields=('id','email','name','password')
        

class StudentSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=50)
    roll=serializers.IntegerField()
    city=serializers.CharField(max_length=50)




# class UserAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=UserAccount
#         fields="__all__"