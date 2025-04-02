from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed')])
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="projects")

    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('done', 'Done')])

    def __str__(self):
        return f"{self.title} - {self.status}"
