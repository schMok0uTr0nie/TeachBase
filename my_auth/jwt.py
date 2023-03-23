from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt

from .models import CustomUser


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")

            username = payload['username']

            user = CustomUser.objects.get(username=username)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is expired, login again')

        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed(
                'Token is invalid')

        except CustomUser.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                'User does not exist')

        return (user, token)
