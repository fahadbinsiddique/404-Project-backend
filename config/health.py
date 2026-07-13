from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.responses import success_response


class HealthCheckView(APIView):
    """GET /api/v1/health/ — quick way to confirm the API is up and reachable."""

    permission_classes = [AllowAny]

    def get(self, request):
        return success_response(
            data={"status": "ok"},
            message="Project 404 API is running.",
        )
