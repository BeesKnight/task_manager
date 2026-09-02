from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    HIGH = 'high'
    NORMAL = 'normal'
    LOW = 'low'

    PRIORITY_CHOICES = [
        (HIGH, 'Высокий'),
        (NORMAL, 'Обычный'),
        (LOW, 'Низкий'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=NORMAL,
    )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
