# recipes/tests/conftest.py
import pytest
from recipes.models import Recipe


@pytest.fixture
def recipe():
    return Recipe.objects.create(
        title="Chocolate Cake",
        slug="chocolate-cake",
        description="Rich & moist.",          # ← no HTML now
        ingredients="flour\neggs\ncocoa",
        instructions="Bake at 350 °F for 30 min.",
    )