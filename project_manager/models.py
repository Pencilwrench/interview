from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed')])

    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('done', 'Done')])

    def __str__(self):
        return f"{self.title} - {self.status}"
        