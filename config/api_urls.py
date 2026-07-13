"""
Aggregates every app's API routes under a single /api/v1/ namespace.

Each app owns its own urls.py; this file only wires them together so the
project root stays clean as new apps are added.

  /api/v1/auth/       -> apps.accounts   (Phase 2)
  /api/v1/tasks/      -> apps.tasks      (Phase 2 / 5)
  /api/v1/images/     -> apps.annotation (Phase 2 / 6)
  /api/v1/polygons/   -> apps.annotation (Phase 2 / 6)
"""

from django.urls import include, path

from .health import HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("auth/", include("apps.accounts.urls")),
    path("", include("apps.tasks.urls")),
    path("", include("apps.annotation.urls")),
]
