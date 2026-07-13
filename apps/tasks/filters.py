import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):
    """
    Powers `GET /tasks/?date=&status=&priority=` (Part 06 / Part 09
    ADR-02 — filtering happens on the backend, not the client).
    """

    date = django_filters.DateFilter(field_name="selected_date")

    class Meta:
        model = Task
        fields = ["status", "priority"]
