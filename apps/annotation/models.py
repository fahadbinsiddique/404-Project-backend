import uuid

from django.conf import settings
from django.db import models


def image_upload_path(instance, filename):
    return f"uploads/images/{instance.user_id}/{filename}"


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=image_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image {self.id}"


class Polygon(models.Model):
    """
    Points are stored as an ordered JSON list of {x, y} pairs, relative
    to the image itself (not the viewport) — see Part 10, ADR-02/03.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="polygons")
    points = models.JSONField()
    color = models.CharField(max_length=7, default="#6366F1")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["image"])]

    def __str__(self):
        return f"Polygon {self.id} on image {self.image_id}"
