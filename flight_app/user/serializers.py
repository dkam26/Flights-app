from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (  'password', 'name', 'email','passport_photograh')

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,required=True)
    password = serializers.CharField(max_length=128,required=True)

    class Meta:
        model = User
        fields = ('password', 'email')


class ChangeSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    class Meta:
        fields = ('file')