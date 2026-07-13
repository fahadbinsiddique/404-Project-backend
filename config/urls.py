"""
Root URL configuration.

Feature-specific URLs are namespaced under /api/v1/ and will be included
app-by-app as each module is implemented (accounts in Phase 2, tasks and
annotation in later phases).
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("config.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
