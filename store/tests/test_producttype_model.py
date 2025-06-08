# store/tests/test_producttype.py

import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.urls import reverse
from store.models import ProductType


@pytest.mark.django_db
def test_str(producttype_blue):
    assert str(producttype_blue) == "Cheese – Blue cheese"


@pytest.mark.django_db
def test_unique_together(category_cheese):
    # first one OK
    ProductType.objects.create(
        title="Soft",
        slug="soft",
        category=category_cheese,
    )
    # duplicate (title, category) pair should fail
    with pytest.raises(IntegrityError):
        ProductType.objects.create(
            title="Soft",
            slug="soft-dupe",
            category=category_cheese,
        )


@pytest.mark.django_db
def test_same_title_different_category(category_cheese, category_bread):
    # allowed because the category differs
    ProductType.objects.create(
        title="Artisan",
        slug="artisan-cheese",
        category=category_cheese,
    )
    ProductType.objects.create(
        title="Artisan",
        slug="artisan-bread",
        category=category_bread,
    )
    assert ProductType.objects.filter(title="Artisan").count() == 2


@pytest.mark.django_db
def test_protected_delete(category_cheese, producttype_blue):
    # deleting the category should raise ProtectedError
    with pytest.raises(ProtectedError):
        category_cheese.delete()