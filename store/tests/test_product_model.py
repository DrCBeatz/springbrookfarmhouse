# store/tests/test_product_model.py
import pytest
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.urls import reverse

from store.models import (
    Product,
    Producer,
    Category,
    ProductType,
)


# ──────────────────────────────
#  fixtures
# ──────────────────────────────
@pytest.fixture
def producer(sample_image):
    return Producer.objects.create(
        name="Spring Brook",
        slug="spring-brook",
        image=sample_image,
    )


@pytest.fixture
def category():
    return Category.objects.create(
        title="Cheese", slug="cheese", is_taxable=True
    )


@pytest.fixture
def product_type(category):
    return ProductType.objects.create(
        title="Hard",
        slug="hard",
        category=category,
        enabled=True,
    )


@pytest.fixture
def product(producer, category, product_type, sample_image):
    return Product.objects.create(
        title="Comté",
        slug="comte",
        description="A classic French alpine cheese.",
        category=category,
        product_type=product_type,
        producer=producer,
        price=Decimal("12.50"),
        stock=5,
        image=sample_image,
        enabled=True,
    )


# ──────────────────────────────
#  basic behaviour
# ──────────────────────────────
@pytest.mark.django_db
def test_str(product):
    assert str(product) == "Comté"


@pytest.mark.django_db
def test_get_absolute_url(product):
    expected = reverse("store:product_detail", kwargs={"slug": "comte"})
    assert product.get_absolute_url() == expected


@pytest.mark.django_db
def test_effective_price_no_discount(product):
    assert product.effective_price == product.price


@pytest.mark.django_db
def test_effective_price_with_discount(product):
    product.has_discount = True
    product.discount_price = Decimal("9.99")
    product.save()

    assert product.effective_price == Decimal("9.99")


# ──────────────────────────────
#  DB-level constraints
# ──────────────────────────────
@pytest.mark.django_db
def test_negative_price_not_allowed(producer, category, product_type, sample_image):
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Product.objects.create(
                title="Bad Price",
                slug="bad-price",
                category=category,
                product_type=product_type,
                producer=producer,
                price=Decimal("-1.00"),
            )


@pytest.mark.django_db
def test_discount_must_be_lower_than_price(producer, category, product_type):
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Product.objects.create(
                title="Wrong Discount",
                slug="wrong-discount",
                category=category,
                product_type=product_type,
                producer=producer,
                price=Decimal("10.00"),
                has_discount=True,
                discount_price=Decimal("12.00"),   # ≥ price → violates constraint
            )


# ──────────────────────────────
#  ordering
# ──────────────────────────────
@pytest.mark.django_db
def test_default_ordering_alphabetical(product, producer, category, product_type):
    Product.objects.create(
        title="Brie",
        slug="brie",
        category=category,
        product_type=product_type,
        producer=producer,
        price=Decimal("8.00"),
    )
    titles = list(Product.objects.values_list("title", flat=True))
    assert titles == ["Brie", "Comté"]     # ordering = ['title']


# ──────────────────────────────
#  ImageKit specs
# ──────────────────────────────
@pytest.mark.django_db
def test_image_specs_exist(product):
    # force creation of renditions
    product.preview.generate()
    product.thumbnail.generate()

    assert product.preview.storage.exists(product.preview.name)
    assert product.thumbnail.storage.exists(product.thumbnail.name)