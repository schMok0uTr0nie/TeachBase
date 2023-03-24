from rest_framework import serializers
from .models import *


class CreateUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=50)

    name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    role_id = serializers.IntegerField(default=1, help_text='1 - listener, 2 - specialist, 4 - manager')
    auth_type = serializers.IntegerField(default=0, help_text='0 - login/pass, 1 - LDAP, 2 - SAML')
    lang = serializers.CharField(max_length=20, help_text='ru')


class SessionRegisterSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    email = serializers.CharField(max_length=255, allow_blank=True)
    phone = serializers.CharField(max_length=20, allow_blank=True)
    user_id = serializers.IntegerField(allow_null=True)


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
