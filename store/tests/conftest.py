# store/tests/conftest.py
import io
from PIL import Image
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from store.models import Producer, Category, ProductType
from django.utils.text import slugify

# ---------------- shared utility ---------------------------------
@pytest.fixture
def sample_image():
    buf = io.BytesIO()
    Image.new("RGB", (200, 200), color="red").save(buf, format="JPEG")
    buf.seek(0)
    return SimpleUploadedFile("test.jpg", buf.read(), content_type="image/jpeg")


# ---------------- producer objects -------------------------------
@pytest.fixture
def producer_active(sample_image):
    return Producer.objects.create(
        name="Spring Brook",
        slug="spring-brook",
        image=sample_image,
        description="Award-winning dairy farm.",
    )


@pytest.fixture
def producer_inactive(sample_image):
    return Producer.objects.create(
        name="Hidden Farm",
        slug="hidden-farm",
        image=sample_image,
        is_active=False,
    )


@pytest.fixture
def six_active_producers(sample_image):
    return [
        Producer.objects.create(
            name=f"Farm {i}",
            slug=f"farm-{i}",
            image=sample_image,
        )
        for i in range(6)
    ]

# ---------------- category and producttype objects ----------------

@pytest.fixture
def category_cheese():
    """An active, taxable category."""
    return Category.objects.create(
        title="Cheese",
        slug=slugify("Cheese"),
        is_taxable=True,
        producer_cut=0.80,  # handy for assertions
    )


@pytest.fixture
def category_bread():
    """A second category so we can test unique_together rules."""
    return Category.objects.create(
        title="Bread",
        slug=slugify("Bread"),
        is_taxable=False,
    )


@pytest.fixture
def producttype_blue(category_cheese):
    """Sample ProductType → Cheese."""
    return ProductType.objects.create(
        title="Blue cheese",
        slug=slugify("Blue cheese"),
        category=category_cheese,
    )