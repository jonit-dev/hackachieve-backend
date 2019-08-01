from django.db import models

from apps.checklists.models import Checklist
from apps.projects.models import Project
from apps.users.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    checklist = models.ForeignKey(
        Checklist, on_delete=models.CASCADE, default=None, null=True)
    description = models.TextField(null=True)
    deadline = models.DateTimeField(null=True)
    priority = models.IntegerField(default=0, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):  # title on dashboard
        return self.title
