from rest_framework import serializers

from core.api.serializers import BaseSerializer
from .models import Project


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

