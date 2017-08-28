
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from drf_auth.core.serializers import LoginSerializer
from drf_auth.core.serializers import UserSerializer


class LoginView(viewsets.ViewSet):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response({'token': serializer.get_token()}, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors}, status=422)


class UserView(viewsets.ViewSet):

    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(instance=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

