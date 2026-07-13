from django.urls import path

from .views import TaskDetailView, TaskListCreateView, TaskStatusUpdateView

app_name = "tasks"

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<uuid:id>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<uuid:id>/status/", TaskStatusUpdateView.as_view(), name="task-status-update"),
]
