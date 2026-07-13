from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.tasks.models import Task

DEMO_EMAIL = "demo@project404.com"

SAMPLE_TASKS = [
    {
        "title": "Design homepage layout",
        "description": "Draft the hero section and navigation for the marketing site.",
        "status": Task.Status.TODO,
        "priority": Task.Priority.HIGH,
        "tags": ["UI", "Design"],
        "day_offset": 0,
    },
    {
        "title": "Set up CI pipeline",
        "description": "Add lint and type-check steps to the GitHub Actions workflow.",
        "status": Task.Status.TODO,
        "priority": Task.Priority.MEDIUM,
        "tags": ["DevOps"],
        "day_offset": 0,
    },
    {
        "title": "Implement JWT refresh flow",
        "description": "Wire up the Axios interceptor to refresh expired access tokens.",
        "status": Task.Status.IN_PROGRESS,
        "priority": Task.Priority.HIGH,
        "tags": ["Backend", "Auth"],
        "day_offset": 0,
    },
    {
        "title": "Write backend README",
        "description": "Document setup steps and environment variables.",
        "status": Task.Status.DONE,
        "priority": Task.Priority.LOW,
        "tags": ["Docs"],
        "day_offset": 0,
    },
    {
        "title": "Review polygon validation rules",
        "description": "Double-check minimum point count and color format checks.",
        "status": Task.Status.TODO,
        "priority": Task.Priority.MEDIUM,
        "tags": ["Backend", "Annotation"],
        "day_offset": 1,
    },
]


class Command(BaseCommand):
    help = "Seeds sample tasks for the demo user (run seed_demo_user first)."

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            demo_user = User.objects.get(email=DEMO_EMAIL)
        except User.DoesNotExist as exc:
            raise CommandError(
                "Demo user not found. Run `python manage.py seed_demo_user` first."
            ) from exc

        today = timezone.localdate()
        created_count = 0

        for sample in SAMPLE_TASKS:
            selected_date = today + timedelta(days=sample["day_offset"])
            _, created = Task.objects.get_or_create(
                user=demo_user,
                title=sample["title"],
                selected_date=selected_date,
                defaults={
                    "description": sample["description"],
                    "status": sample["status"],
                    "priority": sample["priority"],
                    "tags": sample["tags"],
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {created_count} sample task(s) for {DEMO_EMAIL}.")
        )
