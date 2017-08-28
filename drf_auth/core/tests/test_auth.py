import base64

from itsdangerous import TimedJSONWebSignatureSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from drf_auth.core.auth import TokenAuthenticate

User = get_user_model()


class TokenAuthenticateTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token_authenticate = TokenAuthenticate()
        self.request = APIRequestFactory()
        self.request.path = '/'
        self.serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=settings.EXPIRES_IN)
        self.payload = {'username': self.user.username, 'password': 'test'}
        self.token = self.serializer.dumps(self.payload)
        self.token_base64 = base64.b64encode(self.token).decode('utf-8')

    def test_verify_token(self):
        self.assertDictEqual(self.token_authenticate.verify_token(self.token), self.payload)

    def test_authenticate_is_not_basic(self):
        with self.assertRaises(AuthenticationFailed):
            self.request.META = {
                "HTTP_AUTHORIZATION": 'not-basic'
            }
            self.token_authenticate.authenticate(self.request)

    def test_authenticate_is_not_base64(self):
        with self.assertRaises(AuthenticationFailed):
            self.request.META = {
                "HTTP_AUTHORIZATION": 'basic not-base64'
            }
            self.token_authenticate.authenticate(self.request)

    def test_authenticate(self):
        self.request.META = {
            "HTTP_AUTHORIZATION": 'Basic %s' % self.token_base64
        }

        self.assertIsInstance(self.token_authenticate.authenticate(self.request)[0], User)
        self.assertIsNone(self.token_authenticate.authenticate(self.request)[1])

    # def test_authenticate_credentials_is_anonymous_user(self):
    #     self.assertIsInstance(self.token_authenticate.authenticate_credentials(anonymous=True)[0], AnonymousUser)

    # def test_authenticate_credentials_user_does_not_exists(self):
    #     with self.assertRaises(AuthenticationFailed):
    #         payload = {'username': 'test2', 'password': 'test2'}
    #         self.token_authenticate.authenticate_credentials(payload=payload)

    # def test_authenticate_credentials(self):
    #     self.assertIsInstance(self.token_authenticate.authenticate_credentials(payload=self.payload)[0], User)
