# store/views.py

from django.views.generic import ListView, DetailView
from .models import Producer, Product

# ──────────────────────────────
#  Producer
# ──────────────────────────────
class ProducerListView(ListView):
    model               = Producer
    template_name       = "store/producer_list.html"
    context_object_name = "producers"
    paginate_by         = 6

    def get_queryset(self):
        # only show active producers, alphabetical (defined in Meta.ordering)
        return Producer.objects.filter(is_active=True)


class ProducerDetailView(DetailView):
    model               = Producer
    template_name       = "store/producer_detail.html"
    context_object_name = "producer"

    def get_queryset(self):
        # keeps 404 behaviour if slug is inactive
        return Producer.objects.filter(is_active=True)

# ──────────────────────────────
#  Product
# ──────────────────────────────
class ProductListView(ListView):
    model               = Product
    template_name       = "store/product_list.html"
    context_object_name = "products"
    paginate_by         = 12

    def get_queryset(self):
        """
        Show only enabled items. `select_related` pulls the FK rows in one query
        so the list view stays fast.
        """
        return (
            Product.objects.filter(enabled=True)
            .select_related("category", "producer", "product_type")
        )


class ProductDetailView(DetailView):
    model               = Product
    template_name       = "store/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        """Keep 404 behaviour for disabled products."""
        return (
            Product.objects.filter(enabled=True)
            .select_related("category", "producer", "product_type")
        )