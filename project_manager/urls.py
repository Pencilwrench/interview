from django.urls import include, path

from . import views as api_views

project_urlpatterns = [
    path(
        "projects/list/",
        api_views.ProjectListAPIView.as_view(),
        name="projects_list",
    ),
    path(
        "tasks/list/",
        api_views.TaskListAPIView.as_view(),
        name="tasks_list",
    ),
    path(
        "tasks/bulk-assign/",
        api_views.BulkTaskAssignmentView.as_view(),
        name="bulk_task_assignment",
    ),
]

urlpatterns = project_urlpatterns
