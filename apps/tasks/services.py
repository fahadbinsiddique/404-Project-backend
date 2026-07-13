"""
Service layer for the tasks app.

Views stay thin and delegate any logic beyond simple serialization here.
Right now the operations are simple CRUD, but keeping this boundary in
place means future rules (e.g. notifying on overdue tasks, enforcing
max tasks per day) have an obvious home without reshaping the views.
"""

from .models import Task


def create_task(*, user, validated_data) -> Task:
    return Task.objects.create(user=user, **validated_data)


def update_task_status(*, task: Task, status: str) -> Task:
    task.status = status
    task.save(update_fields=["status", "updated_at"])
    return task
