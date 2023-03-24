from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course
from .serializers import CourseSerializer


class CourseDBAPIView(APIView):

    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if id:
            try:
                courses = Course.objects.get(id=id)
                serializer = CourseSerializer(courses)
            except:
                return Response({'error': f'Course with ID: {id} does not exist!'})
        else:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)
