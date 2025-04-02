from django.contrib import admin

from .models import Project, Task, Team


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "due_date", "assigned_to")
    list_filter = ("status", "due_date", "assigned_to")
    search_fields = ("title", "description")


admin.site.register(Project)
admin.site.register(Task, TaskAdmin)
admin.site.register(Team)
