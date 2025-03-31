from django.contrib import admin
from django.contrib.auth.models import User
from functools import cached_property

from .models import Project, Task, Team


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "due_date", "assigned_to")
    list_filter = ("status", "due_date", "assigned_to")
    search_fields = ("title", "description")
    
    @cached_property
    def _get_project(self):
        if not hasattr(self, '_task_id'):
            return None
        return Project.objects.filter(tasks__id=self._task_id).select_related("team").first()
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "assigned_to" and request.resolver_match and "object_id" in request.resolver_match.kwargs:
            self._task_id = request.resolver_match.kwargs["object_id"]
            project = self._get_project
            if project and project.team_id:
                formfield.queryset = User.objects.filter(team__id=project.team_id)
        return formfield


admin.site.register(Project)
admin.site.register(Task, TaskAdmin)
admin.site.register(Team)
