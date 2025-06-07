# store/urls.py

from django.urls import path
from .views import ProducerListView, ProducerDetailView

app_name = "store"

urlpatterns = [
    path("producers/",ProducerListView.as_view(),name="producer_list"),
    path("producers/<slug:slug>/",ProducerDetailView.as_view(),name="producer_detail"),
]