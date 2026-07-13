"""
Annotation views.

Ownership is enforced the same way as in the tasks app: every queryset
is scoped to the authenticated user (directly for images, and via the
related `image__user` for polygons).
"""

from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.common.responses import success_response

from .models import Image, Polygon
from .serializers import ImageSerializer, ImageUploadSerializer, PolygonSerializer
from .services import create_polygon, save_uploaded_image


class ImageListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/images/
    POST /api/v1/images/   (multipart/form-data, field name: "image")
    """

    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return ImageUploadSerializer if self.request.method == "POST" else ImageSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ImageSerializer(queryset, many=True, context=self.get_serializer_context())
        return success_response(serializer.data, message="Images retrieved successfully.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = save_uploaded_image(
            user=request.user, image_file=serializer.validated_data["image"]
        )
        output = ImageSerializer(image, context=self.get_serializer_context())
        return success_response(
            output.data, message="Image uploaded successfully.", status_code=201
        )


class ImagePolygonListView(generics.ListAPIView):
    """GET /api/v1/images/{image_id}/polygons/"""

    serializer_class = PolygonSerializer

    def get_queryset(self):
        return Polygon.objects.filter(
            image__id=self.kwargs["image_id"], image__user=self.request.user
        )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(serializer.data, message="Polygons retrieved successfully.")


class PolygonCreateView(generics.CreateAPIView):
    """POST /api/v1/polygons/"""

    serializer_class = PolygonSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        polygon = create_polygon(
            image=serializer.validated_data["image"],
            color=serializer.validated_data.get("color", "#6366F1"),
            points=serializer.validated_data["points"],
        )
        output = self.get_serializer(polygon)
        return success_response(
            output.data, message="Polygon saved successfully.", status_code=201
        )


class PolygonDeleteView(generics.DestroyAPIView):
    """DELETE /api/v1/polygons/{id}/"""

    serializer_class = PolygonSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Polygon.objects.filter(image__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
