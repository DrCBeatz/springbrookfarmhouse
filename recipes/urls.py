# recipes/views.py
from django.urls import path
from .views import RecipeListView, RecipeDetailView

app_name = "recipes"

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("<slug:slug>/", RecipeDetailView.as_view(), name="recipe_detail"),
]