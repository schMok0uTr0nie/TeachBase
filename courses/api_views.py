import os

from rest_framework import permissions, status
from rest_framework.response import Response
import requests
import json

from rest_framework.views import APIView

from my_auth.models import CustomUser
from .serializers import *
from dotenv import load_dotenv

load_dotenv()


def obtain_token():
    """ Возвращает токен для запросов к Teachbase API """

    OAUTH_URL = "https://go.teachbase.ru/oauth/token"
    payload = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'grant_type': 'client_credentials'
    }

    res = requests.post(f'{OAUTH_URL}', data=payload)
    token = res.json()['access_token']
    return token


class CreateUserAPIView(APIView):
    """ Создаем нового пользователя на стороне Teachbase API """

    serializer_class = CreateUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        endpoint = '/users/create'
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            phone = serializer.validated_data["phone"]

            try:
                user = CustomUser.objects.get(email=email)
                user.phone = phone
            except:
                user = None

            token = obtain_token()

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            payload = {
                "users": [
                    serializer.validated_data
                ]
            }

            res = requests.post(f'{os.getenv("URL")}/{endpoint}', headers=headers, data=json.dumps(payload))

            if user:
                user.teachbase_user_id = res.json()['id']

            return Response(res.json(), status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionRegisterAPIView(APIView):
    """ Запись пользователя на сессию выбранного курса """

    serializer_class = SessionRegisterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = request.user

        if serializer.is_valid():
            session_id = serializer.validated_data["session_id"]
            email = serializer.validated_data["email"]
            phone = serializer.validated_data["phone"]
            user_id = serializer.validated_data["user_id"]

            if not email:
                email = user.email
            if not phone:
                phone = user.phone
            if not user_id:
                user_id = user.teachbase_user_id

            endpoint = f'/course_sessions/{session_id}/register'

            token = obtain_token()

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            payload = {
                'email': email,
                'phone': phone,
                'user_id': user_id
            }

            res = requests.post(f'{os.getenv("URL")}/{endpoint}', headers=headers, data=payload)

            return Response([res.json(),
                             serializer.data,
                            {'msg': f'\nПользователь {user_id} успешно зарегистрирован на сессию!'}],
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseAPIView(APIView):
    """ Получение списка курсов от Teachbase API """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None):
        endpoint = '/courses/'

        token = obtain_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        if id:
            endpoint += f'{id}'

        res = requests.get(f'{os.getenv("URL")}/{endpoint}', headers=headers)
        if res.status_code == 200 and not id:
            for course in res.json():
                try:
                    db_course = Course.objects.get(id=course["id"])
                    db_course.delete()
                except Exception:
                    pass

                Course.objects.create(
                    id=course["id"],
                    name=course["name"],
                    created_at=course["created_at"],
                    updated_at=course["updated_at"],
                    owner_id=course["owner_id"],
                    owner_name=course["owner_name"],
                    description=course["description"],
                    total_score=course["total_score"],
                    total_tasks=course["total_tasks"],
                    unchangeable=course["unchangeable"],
                    include_weekly_report=course["include_weekly_report"],
                    content_type=course["content_type"],
                    is_netology=course["is_netology"],
                    demo=course["demo"],
                    custom_author_names=course["custom_author_names"],
                    custom_contents_link=course["custom_contents_link"],
                    duration=course["duration"]
                )

        return Response(res.json(), status=res.status_code)


class CourseSessionAPIView(APIView):
    """ Получение списка курсов от Teachbase API """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None):
        endpoint = f'/courses/{id}/course_sessions?filter=active'

        token = obtain_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        res = requests.get(f'{os.getenv("URL")}/{endpoint}', headers=headers)

        return Response(res.json(), status=res.status_code)
