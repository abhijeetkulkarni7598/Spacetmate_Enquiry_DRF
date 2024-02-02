from rest_framework import serializers
from . models import *
from app.serializers import *
from django import forms
class EnquireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enquire
        fields = '__all__'
    user = forms.ModelChoiceField(
        queryset=UserAccount.objects.filter(is_customer=True),
        label="User",
    )
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['user'] = UserSerializer(instance.user).data
    #     return representation

class DesignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Design
        fields =  '__all__'



