"""
Authentication views.

`User.USERNAME_FIELD` is set to "email" (see models.py), so
`TokenObtainPairSerializer` already expects an `email` field on input —
no field renaming needed. We subclass it only to attach the logged-in
user's basic info to the token response, and wrap both views so their
output matches the project-wide `{ success, message, data }` envelope
(Part 06 / Part 08).
"""

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.common.responses import success_response

from .serializers import UserSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class LoginView(TokenObtainPairView):
    """POST /api/v1/auth/login/"""

    permission_classes = [AllowAny]
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(
            data=serializer.validated_data,
            message="Login successful.",
        )


class RefreshView(TokenRefreshView):
    """POST /api/v1/auth/refresh/"""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(
            data=serializer.validated_data,
            message="Token refreshed successfully.",
        )
