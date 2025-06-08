# store/admin.py
from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from djrichtextfield.widgets import RichTextWidget

from .models import Producer, Category, ProductType, Product


# ──────────────────────────────
#  Producer
# ──────────────────────────────
@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display   = ("thumb", "name", "is_active", "created_at")
    list_filter    = ("is_active", "created_at")
    search_fields  = ("name", "description")
    ordering       = ("name",)

    prepopulated_fields = {"slug": ("name",)}
    readonly_fields     = ("preview_tag", "created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("name", "slug", "description", "content", "is_active")
        }),
        ("Media", {
            "fields": ("image", "preview_tag", "video_url")
        }),
        ("Links", {
            "fields": ("website_url", "instagram_url", "facebook_url"),
            "classes": ("collapse",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    formfield_overrides = {
        models.TextField: {"widget": RichTextWidget},
    }

    # helpers ----------
    def thumb(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="60" height="60" />',
                               obj.thumbnail.url)
        return "—"
    thumb.short_description = "Thumb"

    def preview_tag(self, obj):
        if obj.preview:
            return format_html('<img src="{}" style="max-width:300px;" />',
                               obj.preview.url)
        return "—"


# ──────────────────────────────
#  Category   ➜  inline ProductTypes
# ──────────────────────────────
class ProductTypeInline(admin.TabularInline):
    """Edit ProductTypes inside the Category page."""
    model = ProductType
    extra = 1
    show_change_link = True
    fields = ("title", "enabled")
    ordering = ("title",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_taxable", "producer_cut")
    list_filter  = ("is_active", "is_taxable")
    search_fields = ("title",)
    ordering = ("title",)

    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ()

    inlines = (ProductTypeInline,)

    fieldsets = (
        (None, {"fields": ("title", "slug", "is_active")}),
        ("Financial", {"fields": ("is_taxable", "producer_cut")}),
    )


# ──────────────────────────────
#  ProductType  (stand-alone list)
# ──────────────────────────────
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display  = ("title", "category", "enabled")
    list_filter   = ("enabled", "category")
    search_fields = ("title",)
    ordering      = ("category__title", "title")

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category",)

    readonly_fields = ("created_at",)


# ──────────────────────────────
#  Product
# ──────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display   = (
        "thumb", "title", "category", "product_type", "producer",
        "price", "has_discount", "discount_price", "stock", "enabled",
        "updated_at",
    )
    list_filter    = (
        "enabled", "has_discount", "category", "product_type", "producer",
        "is_inventory_item", "eligible_for_delivery",
    )
    list_editable  = ("price", "discount_price", "stock", "enabled")
    search_fields  = ("title", "slug", "description",
                      "category__title", "product_type__title", "producer__name")
    autocomplete_fields = ("category", "product_type", "producer", "featured_recipe")
    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ("preview_tag", "created_at", "updated_at")
    ordering        = ("title",)
    list_select_related = ("category", "product_type", "producer")

    fieldsets = (
        (None, {
            "fields": (
                ("title", "slug"),
                ("category", "product_type", "producer"),
                "description",
            )
        }),
        ("Pricing & inventory", {
            "fields": (
                ("price", "has_discount", "discount_price"),
                ("stock", "is_inventory_item", "eligible_for_delivery"),
                "enabled",
            )
        }),
        ("Media", {
            "fields": ("image", "preview_tag", "anchor"),
        }),
        ("Extras", {
            "fields": ("featured_recipe",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    # --- helpers -------------------------------------------------------------
    def thumb(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="45" height="45" style="object-fit:cover;" />',
                obj.thumbnail.url,
            )
        return "—"
    thumb.short_description = "Thumb"
    thumb.admin_order_field = "title"

    def preview_tag(self, obj):
        if obj.preview:
            return format_html('<img src="{}" style="max-width:300px;" />', obj.preview.url)
        return "—"

    # Speed up changelist with only the columns we need
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("category", "product_type", "producer") 