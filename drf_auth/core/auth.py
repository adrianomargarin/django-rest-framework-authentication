
import base64

from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer

from rest_framework.authentication import get_authorization_header
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from django.conf import settings
from django.core.urlresolvers import resolve
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class TokenAuthenticate(BasicAuthentication):
    """
    Custom auth method to authenticate the user trought the token
    """

    ALLOWED_PATHS = [
        'login',
    ]

    def allowed_path(self, request):
        """
        If the anonymous user is tryng to access a valid url
        """
        return resolve(request.path).url_name in self.ALLOWED_PATHS

    def verify_token(self, token):
        try:
            return TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=settings.EXPIRES_IN).loads(token)
        except (BadSignature, SignatureExpired):
            raise AuthenticationFailed('Bad credentials.')

    def authenticate(self, request, simple=False):
        auth = get_authorization_header(request).split()

        if not auth and self.allowed_path(request):
            return self.authenticate_credentials(anonymous=True)

        if not auth or auth[0].lower() != b'basic':
            raise AuthenticationFailed('Bad Credentials.')

        try:
            auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
        except (IndexError, TypeError, base64.binascii.Error):
            raise AuthenticationFailed('Bad Credentials.')

        token, password = auth_parts[0], auth_parts[2]
        payload = self.verify_token(token)

        return self.authenticate_credentials(payload, password, request=request)

    def authenticate_credentials(self, payload=None, password=None, anonymous=False, request=None):
        """
        Authenticate the userid and password against username and password.
        """
        if anonymous:
            return (AnonymousUser(), None)

        credentials = {
            'username': payload['username'],
            'password': payload['password']
        }

        user = authenticate(**credentials)

        if user is None:
            raise AuthenticationFailed('Bad Credentials.')

        if not user.is_active:
            raise AuthenticationFailed('Bad Credentials.')

        return (user, None)


class IsUserAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, User) or isinstance(request.user, AnonymousUser):
            return True

        return False
