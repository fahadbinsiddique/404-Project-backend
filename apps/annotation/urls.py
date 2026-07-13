from django.urls import path

from .views import (
    ImageListCreateView,
    ImagePolygonListView,
    PolygonCreateView,
    PolygonDeleteView,
)

app_name = "annotation"

urlpatterns = [
    path("images/", ImageListCreateView.as_view(), name="image-list-create"),
    path("images/<uuid:image_id>/polygons/", ImagePolygonListView.as_view(), name="image-polygons"),
    path("polygons/", PolygonCreateView.as_view(), name="polygon-create"),
    path("polygons/<uuid:id>/", PolygonDeleteView.as_view(), name="polygon-delete"),
]
