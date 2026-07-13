from rest_framework import serializers

from .models import Image, Polygon


class ImageSerializer(serializers.ModelSerializer):
    """Read representation — used for list responses and after upload."""

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["id", "image_url", "uploaded_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.image:
            return None
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url


class ImageUploadSerializer(serializers.ModelSerializer):
    """Write representation — accepts multipart/form-data with an `image` field."""

    ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
    MAX_FILE_SIZE_MB = 10

    class Meta:
        model = Image
        fields = ["id", "image"]
        read_only_fields = ["id"]

    def validate_image(self, value):
        if value.content_type not in self.ALLOWED_CONTENT_TYPES:
            raise serializers.ValidationError(
                "Unsupported image type. Use JPG, PNG, or WEBP."
            )
        max_bytes = self.MAX_FILE_SIZE_MB * 1024 * 1024
        if value.size > max_bytes:
            raise serializers.ValidationError(
                f"Image must be smaller than {self.MAX_FILE_SIZE_MB}MB."
            )
        return value


class PolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygon
        fields = ["id", "image", "color", "points", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_points(self, value):
        if not isinstance(value, list) or len(value) < 3:
            raise serializers.ValidationError("A polygon requires at least 3 points.")
        for point in value:
            if (
                not isinstance(point, dict)
                or "x" not in point
                or "y" not in point
                or not isinstance(point["x"], (int, float))
                or not isinstance(point["y"], (int, float))
            ):
                raise serializers.ValidationError(
                    "Each point must be an object with numeric 'x' and 'y'."
                )
        return value

    def validate_color(self, value):
        if not value.startswith("#") or len(value) not in (4, 7):
            raise serializers.ValidationError("Color must be a valid hex code, e.g. #6366F1.")
        return value

    def validate_image(self, value):
        request = self.context.get("request")
        if request and value.user_id != request.user.id:
            raise serializers.ValidationError("You do not own this image.")
        return value
