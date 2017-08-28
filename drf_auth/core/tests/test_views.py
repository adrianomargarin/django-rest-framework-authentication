
import json
import base64

from itsdangerous import TimedJSONWebSignatureSerializer

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

User = get_user_model()


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_login_valid(self):
        data = {'username': self.user.username, 'password': 'test'}
        response = self.client.post(reverse_lazy('login'), data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['token'])

    def test_login_invalid(self):
        response = self.client.post(reverse_lazy('login'), data=json.dumps({}), content_type='application/json')

        self.assertEqual(response.status_code, 422)


class UserViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=settings.EXPIRES_IN)
        token = serializer.dumps({'username': self.user.username, 'password': 'test'}).decode('utf-8')
        token_base64 = base64.b64encode(token.encode('utf-8')).decode('utf-8')

        self.headers = {
            'HTTP_AUTHORIZATION': 'Basic {}'.format(token_base64)
        }

    def test_get(self):
        response = self.client.get(reverse_lazy('user'), **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'username': self.user.username,
                                               'first_name': self.user.first_name,
                                               'last_name': self.user.last_name})
