# store/tests/test_category_model.py
import pytest
from django.urls import reverse
from store.models import Category


@pytest.mark.django_db
def test_str(category_cheese):
    assert str(category_cheese) == "Cheese"

@pytest.mark.django_db
def test_unique_title_constraint(category_cheese):
    with pytest.raises(Exception):
        Category.objects.create(
            title="Cheese",
            slug="cheese-dupe",
        )