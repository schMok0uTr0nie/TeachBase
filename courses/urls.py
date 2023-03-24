from django.urls import path
from .api_views import *
from .views import *


urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view(), name='create_user'),
    path('session_register/', SessionRegisterAPIView.as_view(), name='register_on_session'),
    path('courses/', CourseAPIView.as_view(), name='show_all_courses'),
    path('courses/<int:id>', CourseAPIView.as_view(), name='show_course'),
    path('courses/<int:id>/sessions/', CourseSessionAPIView.as_view(), name='get_course_sessions'),
    path('db/courses/', CourseDBAPIView.as_view(), name='show_db_courses'),
    path('db/courses/<int:id>', CourseDBAPIView.as_view(), name='show_db_course')
]
