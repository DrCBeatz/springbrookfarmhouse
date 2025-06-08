# store/tests/test_product_views_template.py
import pytest
from decimal import Decimal

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
    return Category.objects.create(title="Cheese", slug="cheese")


@pytest.fixture
def product_type(category):
    return ProductType.objects.create(
        title="Hard", slug="hard", category=category
    )


@pytest.fixture
def product_enabled(producer, category, product_type, sample_image):
    return Product.objects.create(
        title="Comté",
        slug="comte",
        category=category,
        product_type=product_type,
        producer=producer,
        price=Decimal("12.50"),
        stock=3,
        image=sample_image,
        enabled=True,
    )


@pytest.fixture
def product_disabled(producer, category, product_type):
    return Product.objects.create(
        title="Morbier",
        slug="morbier",
        category=category,
        product_type=product_type,
        producer=producer,
        price=Decimal("11.00"),
        enabled=False,
    )


@pytest.fixture
def thirteen_enabled_products(producer, category, product_type):
    """Create 13 products to force pagination (paginate_by = 12)."""
    bulk = [
        Product(
            title=f"Cheese #{i}",
            slug=f"cheese-{i}",
            category=category,
            product_type=product_type,
            producer=producer,
            price=Decimal("5.00") + i,
            enabled=True,
        )
        for i in range(13)
    ]
    Product.objects.bulk_create(bulk)


# ──────────────────────────────
#  list view
# ──────────────────────────────
@pytest.mark.django_db
def test_product_list_status_ok(client, product_enabled):
    resp = client.get(reverse("store:product_list"))
    assert resp.status_code == 200
    assert "store/product_list.html" in {t.name for t in resp.templates}


@pytest.mark.django_db
def test_list_filters_disabled(client, product_enabled, product_disabled):
    resp = client.get(reverse("store:product_list"))
    products = list(resp.context["products"])
    assert products == [product_enabled]
    html = resp.content.decode()
    assert product_enabled.title in html
    assert product_disabled.title not in html


@pytest.mark.django_db
def test_list_pagination(client, thirteen_enabled_products):
    """
    13 enabled items with paginate_by=12 → two pages:
      * page 1 contains 12 products
      * page 2 contains 1 product
    """
    url = reverse("store:product_list")

    # ---- page 1 -------------------------------------------------------------
    resp1 = client.get(url)
    assert resp1.context["is_paginated"] is True
    paginator = resp1.context["paginator"]
    assert paginator.count == 13
    assert paginator.num_pages == 2
    assert len(resp1.context["products"]) == 12   # first 12 items

    # ---- page 2 -------------------------------------------------------------
    resp2 = client.get(url + "?page=2")
    assert resp2.status_code == 200
    assert len(resp2.context["products"]) == 1

# ──────────────────────────────
#  detail view
# ──────────────────────────────
@pytest.mark.django_db
def test_product_detail_ok(client, product_enabled):
    url = reverse("store:product_detail", kwargs={"slug": "comte"})
    resp = client.get(url)
    assert resp.status_code == 200
    assert "store/product_detail.html" in {t.name for t in resp.templates}
    assert product_enabled.title in resp.content.decode()


@pytest.mark.django_db
def test_detail_404_for_disabled(client, product_disabled):
    url = reverse("store:product_detail", kwargs={"slug": "morbier"})
    resp = client.get(url)
    assert resp.status_code == 404


@pytest.mark.django_db
def test_discount_price_rendering(client, producer, category, product_type):
    discounted = Product.objects.create(
        title="Discounted",
        slug="discounted",
        category=category,
        product_type=product_type,
        producer=producer,
        price=Decimal("10.00"),
        has_discount=True,
        discount_price=Decimal("7.50"),
        enabled=True,
    )
    resp = client.get(reverse("store:product_detail", kwargs={"slug": "discounted"}))
    html = resp.content.decode()
    # Shows effective price and (del) regular price
    assert "$7.50" in html
    assert "$10.00" in html