from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "created_at", "is_published", "views_counter")
    search_fields = (
        "title",
        "created_at",
    )
    list_filter = ("is_published", "created_at")
