from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

DEMO_EMAIL = "demo@project404.com"
DEMO_PASSWORD = "Demo@1234"


class Command(BaseCommand):
    help = "Creates (or resets) the demo account used for assignment review."

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            email=DEMO_EMAIL,
            defaults={"is_active": True},
        )
        user.set_password(DEMO_PASSWORD)
        user.is_active = True
        user.save()

        action = "Created" if created else "Reset"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} demo user -> email: {DEMO_EMAIL} | password: {DEMO_PASSWORD}"
            )
        )
