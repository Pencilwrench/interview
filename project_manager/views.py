from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers import BaseListOutputSerializer
from .serializers import ProjectSerializer, TaskSerializer
from .services import ProjectsReadService, TasksReadService


class ProjectListAPIView(APIView):

    class ProjectListOutputSerializer(BaseListOutputSerializer):
        items = ProjectSerializer(many=True)

    def get(self, request) -> Response:
        projects = ProjectsReadService().list()
        output_data = self.ProjectListOutputSerializer.get_output_data(projects)
        return Response(output_data, status=status.HTTP_200_OK)


class TaskListAPIView(APIView):

    class TaskListOutputSerializer(BaseListOutputSerializer):
        items = TaskSerializer(many=True)

    def get(self, request) -> Response:
        tasks = TasksReadService().list()
        output_data = self.TaskListOutputSerializer.get_output_data(tasks)
        return Response(output_data, status=status.HTTP_200_OK)