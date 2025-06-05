# recipes/admin.py
from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from djrichtextfield.widgets import RichTextWidget

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # -------- list view ----------
    list_display   = ("thumbnail_tag", "title", "created_at", "updated_at")
    list_filter    = ("created_at",)
    search_fields  = ("title", "description", "ingredients")
    ordering       = ("-created_at",)

    # -------- detail form --------
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields     = ("preview_tag", "created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": (
                "title",
                "slug",
                "description",
                "image",
                "preview_tag",        # shows after image upload
            )
        }),
        ("Content", {
            "fields": ("ingredients", "instructions"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),  # collapsible section
        }),
    )

    # Replace the plain textarea with TinyMCE for TextFields
    formfield_overrides = {
        models.TextField: {"widget": RichTextWidget},
    }

    # ---------- helpers ----------
    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="60" height="60" />',
                               obj.thumbnail.url)
        return "—"
    thumbnail_tag.short_description = "Thumb"

    def preview_tag(self, obj):
        if obj.preview:
            return format_html('<img src="{}" style="max-width:300px;" />',
                               obj.preview.url)
        return "—"