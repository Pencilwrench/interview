from dataclasses import dataclass
from typing import List, Optional
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Project, Task


@dataclass(frozen=True)
class ProjectList:
    items: list[Project]


@dataclass(frozen=True)
class TaskList:
    items: list[Task]


@dataclass(frozen=True)
class BulkTaskAssignmentResult:
    tasks: List[Task]
    assignee: User
    total_updated: int


class ProjectsReadService:
    def list(self) -> ProjectList:
        return ProjectList(items=Project.objects.all())


class TasksReadService:
    def list(self) -> TaskList:
        return TaskList(items=Task.objects.all())


class TaskAssignmentService:
    """Service for handling task assignments."""
    
    def validate_task_assignment(
        self, 
        task_ids: List[int], 
        user: User
    ) -> None:
        """
        Validate that tasks can be assigned to the user.
        
        Args:
            task_ids: List of task IDs to validate
            user: User to assign tasks to
            
        Raises:
            ValidationError: If validation fails
        """
        if not task_ids:
            raise ValidationError("No tasks provided")
            
        # Validate tasks exist and get their teams
        tasks = Task.objects.filter(
            id__in=task_ids
        ).select_related('project__team')
        
        if len(tasks) != len(task_ids):
            raise ValidationError("One or more tasks do not exist")
            
        # Get user's teams
        user_teams = user.team_set.all()
        
        # Check if user belongs to all task teams
        invalid_tasks = tasks.exclude(project__team__in=user_teams)
        if invalid_tasks.exists():
            raise ValidationError(
                "User cannot be assigned to tasks in teams they don't belong to"
            )
    
    @transaction.atomic
    def bulk_assign(
        self, 
        task_ids: List[int], 
        user: User
    ) -> BulkTaskAssignmentResult:
        """
        Assign multiple tasks to a user in a single transaction.
        
        Args:
            task_ids: List of task IDs to assign
            user: User to assign tasks to
            
        Returns:
            BulkTaskAssignmentResult with updated tasks
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate assignment
        self.validate_task_assignment(task_ids, user)
        
        # Bulk update tasks
        updated_count = Task.objects.filter(
            id__in=task_ids
        ).update(assigned_to=user)
        
        # Fetch updated tasks with related data
        updated_tasks = Task.objects.filter(
            id__in=task_ids
        ).select_related(
            'project',
            'assigned_to'
        )
        
        return BulkTaskAssignmentResult(
            tasks=list(updated_tasks),
            assignee=user,
            total_updated=updated_count
        )