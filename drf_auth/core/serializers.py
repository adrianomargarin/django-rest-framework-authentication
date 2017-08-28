
from itsdangerous import TimedJSONWebSignatureSerializer
from rest_framework import serializers

from django.conf import settings
from django.contrib.auth import get_user_model


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def get_token(self):
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=settings.EXPIRES_IN)

        return serializer.dumps({'username': self.data['username'], 'password': self.data['password']})


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']
