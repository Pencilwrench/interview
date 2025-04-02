from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from core.api.serializers import BaseListOutputSerializer
from .serializers import ProjectSerializer, TaskSerializer, BulkTaskAssignmentSerializer
from .services import ProjectsReadService, TasksReadService
from .models import Task


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


class BulkTaskAssignmentView(APIView):
    def post(self, request):
        serializer = BulkTaskAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            task_ids = serializer.validated_data['task_ids']
            user_id = serializer.validated_data['user_id']
            
            # Get user
            user = get_object_or_404(User, id=user_id)
            
            # Update all tasks
            tasks = []
            for task_id in task_ids:
                task = Task.objects.get(id=task_id)
                task.assigned_to = user
                task.save()
                tasks.append(task)
            
            # Return updated tasks
            return Response({
                'message': f'Successfully assigned {len(tasks)} tasks to {user.username}',
                'tasks': TaskSerializer(tasks, many=True).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)