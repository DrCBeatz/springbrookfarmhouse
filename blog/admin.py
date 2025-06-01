# blog/admin.py
from django.contrib import admin
from .models import BlogPost, BlogPostPhoto


class BlogPostPhotoInline(admin.TabularInline):
    model = BlogPostPhoto
    extra = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "author", "status", "published_at")
    list_filter  = ("status", "author")
    search_fields = ("title", "caption", "content")
    inlines = [BlogPostPhotoInline]
    readonly_fields = ("created_at", "updated_at")