# recipes/views.py
from django.views.generic import ListView, DetailView
from .models import Recipe


class RecipeListView(ListView):
    model               = Recipe
    template_name       = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by         = 6         # tweak to taste


class RecipeDetailView(DetailView):
    model               = Recipe
    template_name       = "recipes/recipe_detail.html"
    context_object_name = "recipe"