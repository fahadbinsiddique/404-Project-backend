from django.contrib import admin

from .models import Image, Polygon


class PolygonInline(admin.TabularInline):
    model = Polygon
    extra = 0
    readonly_fields = ["id", "created_at"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "uploaded_at"]
    search_fields = ["user__email"]
    inlines = [PolygonInline]


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "color", "created_at"]
