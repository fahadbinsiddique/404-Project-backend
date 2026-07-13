"""
Task views.

Every queryset is scoped to `request.user`, which is how ownership is
enforced (Part 05 — Data Ownership Rules / Part 08 — Permission Rules):
a user simply cannot see or affect another user's tasks because they're
never in the queryset to begin with.
"""

from rest_framework import generics
from rest_framework.response import Response

from apps.common.responses import success_response

from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer
from .services import create_task, update_task_status


class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/tasks/?date=&status=&priority=
    POST /api/v1/tasks/
    """

    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data, message="Tasks retrieved successfully.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = create_task(user=request.user, validated_data=serializer.validated_data)
        output = self.get_serializer(task)
        return success_response(
            output.data, message="Task created successfully.", status_code=201
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/tasks/{id}/
    PATCH  /api/v1/tasks/{id}/
    DELETE /api/v1/tasks/{id}/
    """

    serializer_class = TaskSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return success_response(serializer.data, message="Task retrieved successfully.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(serializer.data, message="Task updated successfully.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)


class TaskStatusUpdateView(generics.UpdateAPIView):
    """
    PATCH /api/v1/tasks/{id}/status/

    Dedicated endpoint for drag-and-drop column changes — smaller
    payload and clearer intent than the generic update endpoint
    (Part 06, ADR-01).
    """

    serializer_class = TaskStatusUpdateSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = update_task_status(task=instance, status=serializer.validated_data["status"])
        output = TaskSerializer(task)
        return success_response(output.data, message="Task status updated successfully.")
