
from django.contrib.auth import get_user_model
from django.test import TestCase

from drf_auth.core.serializers import LoginSerializer
from drf_auth.core.serializers import UserSerializer

User = get_user_model()


class LoginSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.serializer_class = LoginSerializer

    def test_serializer_is_valid(self):
        serializer = self.serializer_class(data={'username': self.user.username, 'password': self.user.password})

        self.assertTrue(serializer.is_valid())

    def test_serializer_not_is_valid(self):
        serializer = self.serializer_class(data={})

        self.assertFalse(serializer.is_valid())

    def test_serializer_get_token(self):
        serializer = self.serializer_class(data={'username': self.user.username, 'password': 'test'})

        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.get_token())


class UserSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.serializer_class = UserSerializer

    def test_get_data(self):
        data = self.serializer_class(instance=self.user).data

        self.assertDictEqual(data, {'username': self.user.username,
                                    'first_name': self.user.first_name,
                                    'last_name': self.user.last_name})
