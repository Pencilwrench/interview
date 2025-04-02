from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
import logging

from core.api.serializers import BaseListOutputSerializer
from .serializers import (
    ProjectSerializer,
    TaskSerializer,
    BulkTaskAssignmentInputSerializer,
    BulkTaskAssignmentOutputSerializer
)
from .services import ProjectsReadService, TasksReadService, TaskAssignmentService


logger = logging.getLogger(__name__)


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
    """
    API endpoint for assigning multiple tasks to a user at once.
    
    Requires authentication and appropriate permissions.
    Rate limited to prevent abuse.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def post(self, request) -> Response:
        """
        Assign multiple tasks to a user.
        
        Request body should contain:
        - task_ids: List of task IDs to assign
        - user_id: ID of the user to assign tasks to
        
        Returns:
        - 200: Tasks successfully assigned
        - 400: Invalid input data
        - 401: Not authenticated
        - 403: Permission denied
        - 429: Too many requests
        """
        # Validate input
        input_serializer = BulkTaskAssignmentInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        
        try:
            # Get user
            user = User.objects.get(id=input_serializer.validated_data['user_id'])
            
            # Perform assignment
            result = TaskAssignmentService().bulk_assign(
                task_ids=input_serializer.validated_data['task_ids'],
                user=user
            )
            
            # Log success
            logger.info(
                "User %s assigned %d tasks to %s",
                request.user.username,
                result.total_updated,
                user.username
            )
            
            # Return response
            output_data = BulkTaskAssignmentOutputSerializer.get_output_data(result)
            return Response(output_data, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                "Error in bulk task assignment: %s",
                str(e),
                exc_info=True
            )
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )