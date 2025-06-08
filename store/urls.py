# store/urls.py
from django.urls import path
from .views import ProducerListView, ProducerDetailView, ProductListView, ProductDetailView

app_name = "store"

urlpatterns = [
    path("producers/",ProducerListView.as_view(),name="producer_list"),
    path("producers/<slug:slug>/",ProducerDetailView.as_view(),name="producer_detail"),

    path("products/",                ProductListView.as_view(),   name="product_list"),
    path("products/<slug:slug>/",    ProductDetailView.as_view(), name="product_detail"),
]