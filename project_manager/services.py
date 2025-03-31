from dataclasses import dataclass
from .models import Project, Task


@dataclass(frozen=True)
class ProjectList:
    items: list[Project]


@dataclass(frozen=True)
class TaskList:
    items: list[Task]


class ProjectsReadService:
    def list(self) -> ProjectList:
        return ProjectList(items=Project.objects.all())


class TasksReadService:
    def list(self) -> TaskList:
        return TaskList(items=Task.objects.all())