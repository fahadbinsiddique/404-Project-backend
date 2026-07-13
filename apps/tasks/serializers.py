from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "selected_date",
            "due_date",
            "tags",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_tags(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Tags must be a list of strings.")
        if not all(isinstance(tag, str) for tag in value):
            raise serializers.ValidationError("Every tag must be a string.")
        return value


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Backs the dedicated `PATCH /tasks/{id}/status/` endpoint used by
    drag-and-drop (see Part 06, ADR on the status endpoint).
    """

    class Meta:
        model = Task
        fields = ["status"]
