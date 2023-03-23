from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .jwt import JWTAuthentication
from .serializers import *
from rest_framework import status, permissions


class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIView(GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)
        login(request, user)

        if user:
            response = Response()
            serializer = self.serializer_class(user)
            response.set_cookie(key='jwt', value=user.token, httponly=True)
            response.data = serializer.data
            return response

        return Response({'message': "Invalid credentials, try again!"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        logout(request)
        response.data = {
            'message': 'Successfully logged out!'
        }
        return response
