# store/admin.py
from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from djrichtextfield.widgets import RichTextWidget

from .models import Producer


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    # ---------- list view ----------
    list_display   = ("thumb", "name", "is_active", "created_at")
    list_filter    = ("is_active", "created_at")
    search_fields  = ("name", "description")
    ordering       = ("name",)

    # ---------- detail form ----------
    prepopulated_fields = {"slug": ("name",)}        # auto-fill the slug
    readonly_fields     = ("preview_tag",
                           "created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "slug",
                "description",
                "content",
                "is_active",
            )
        }),
        ("Media", {
            "fields": (
                "image",
                "preview_tag",            # shows once image uploaded
                "video_url",
            )
        }),
        ("Links", {
            "fields": (
                "website_url",
                "instagram_url",
                "facebook_url",
            ),
            "classes": ("collapse",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    # Use TinyMCE for the rich-text field
    formfield_overrides = {
        models.TextField: {"widget": RichTextWidget},
    }

    # ---------- helpers ----------
    def thumb(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="60" height="60" />',
                obj.thumbnail.url,
            )
        return "—"
    thumb.short_description = "Thumb"

    def preview_tag(self, obj):
        if obj.preview:
            return format_html(
                '<img src="{}" style="max-width:300px;" />',
                obj.preview.url,
            )
        return "—"