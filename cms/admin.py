# cms/admin.py
from django.contrib import admin
from .models import HomeCarouselPhoto
from django.utils.html import format_html

@admin.register(HomeCarouselPhoto)
class HomeCarouselPhotoAdmin(admin.ModelAdmin):
    list_display  = ("thumbnail_tag", "title", "order")
    list_editable = ("order",)
    search_fields = ("title",)
    ordering      = ("order", "id")
    readonly_fields = ("preview_tag",)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="60" height="60" />', obj.thumbnail.url)
        return "—"
    thumbnail_tag.short_description = "Thumb"

    def preview_tag(self, obj):
        if obj.preview:
            return format_html('<img src="{}" style="max-width:300px;" />', obj.preview.url)
        return "—"