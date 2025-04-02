from rest_framework import serializers
from django.contrib.auth.models import User

from core.api.serializers import BaseSerializer
from .models import Project, Task
from .services import BulkTaskAssignmentResult


class UserSerializer(BaseSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)


class ProjectSerializer(BaseSerializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    status = serializers.CharField()

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "status",
        ]


class TaskSerializer(BaseSerializer):
    project = ProjectSerializer()
    assigned_to = UserSerializer()

    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    due_date = serializers.DateField()
    status = serializers.CharField()


class BulkTaskAssignmentInputSerializer(serializers.Serializer):
    """
    Serializer for bulk task assignment input.
    """
    task_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="List of task IDs to assign"
    )
    user_id = serializers.IntegerField(
        help_text="ID of the user to assign tasks to"
    )


class BulkTaskAssignmentOutputSerializer(BaseSerializer):
    """
    Serializer for bulk task assignment response.
    """
    items = TaskSerializer(source='tasks', many=True)
    metadata = serializers.SerializerMethodField()

    def get_metadata(self, result: BulkTaskAssignmentResult) -> dict:
        return {
            'total_updated': result.total_updated,
            'assignee': result.assignee.username
        }

    @classmethod
    def get_output_data(cls, result: BulkTaskAssignmentResult) -> dict:
        """Get the formatted output data."""
        serializer = cls(result)
        return {
            'items': serializer.data['items'],
            'metadata': serializer.get_metadata(result)
        }
