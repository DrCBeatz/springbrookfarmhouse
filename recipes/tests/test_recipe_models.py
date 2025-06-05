# recipes/tests/test_recipe_models.py

import pytest
from django.urls import reverse
from recipes.models import Recipe


@pytest.mark.django_db
def test_str(recipe):
    assert str(recipe) == "Chocolate Cake"


@pytest.mark.django_db
def test_get_absolute_url(recipe):
    url = reverse("recipes:recipe_detail", kwargs={"slug": "chocolate-cake"})
    assert recipe.get_absolute_url() == url


@pytest.mark.django_db
def test_ordering():
    r1 = Recipe.objects.create(title="Old",  slug="old")
    r2 = Recipe.objects.create(title="New",  slug="new")
    titles = list(Recipe.objects.values_list("title", flat=True))
    assert titles == ["New", "Old"]          # newest first (ordering meta-option)