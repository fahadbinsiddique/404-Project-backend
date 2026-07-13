from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "status", "priority", "selected_date", "due_date"]
    list_filter = ["status", "priority", "selected_date"]
    search_fields = ["title", "description", "user__email"]
