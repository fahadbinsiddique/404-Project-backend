"""
Service layer for the annotation app. See apps/tasks/services.py for the
rationale — keeps views thin and gives future logic (e.g. auto-deleting
orphaned images, generating thumbnails) an obvious home.
"""

from .models import Image, Polygon


def save_uploaded_image(*, user, image_file) -> Image:
    return Image.objects.create(user=user, image=image_file)


def create_polygon(*, image: Image, color: str, points: list) -> Polygon:
    return Polygon.objects.create(image=image, color=color, points=points)
