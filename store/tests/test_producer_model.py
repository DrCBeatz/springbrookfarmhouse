# store/tests/test_producer_model.py
import pytest
from django.urls import reverse

from store.models import Producer


@pytest.mark.django_db
def test_str(sample_image):
    """__str__ returns the producer’s name."""
    p = Producer.objects.create(
        name="Spring Brook Farm",
        slug="spring-brook-farm",
        image=sample_image,
    )
    assert str(p) == "Spring Brook Farm"


@pytest.mark.django_db
def test_get_absolute_url(sample_image):
    p = Producer.objects.create(
        name="Brook", slug="brook", image=sample_image
    )
    expected = reverse("store:producer_detail", kwargs={"slug": "brook"})
    assert p.get_absolute_url() == expected


@pytest.mark.django_db
def test_default_is_active_flag(sample_image):
    p = Producer.objects.create(name="Active", slug="active", image=sample_image)
    assert p.is_active is True


@pytest.mark.django_db
def test_default_ordering_alphabetical(sample_image):
    Producer.objects.create(name="Zulu", slug="zulu", image=sample_image)
    Producer.objects.create(name="Alpha", slug="alpha", image=sample_image)

    names = list(Producer.objects.values_list("name", flat=True))
    assert names == ["Alpha", "Zulu"]        # ordering = ['name']


@pytest.mark.django_db
def test_image_specs_exist(sample_image, settings):
    """
    ImageKit should generate and store the preview/thumbnail files.
    Works both for local FS and S3 back-ends.
    """
    p = Producer.objects.create(
        name="Pic", slug="pic", image=sample_image
    )
    # generate() forces creation in tests
    p.preview.generate()
    p.thumbnail.generate()

    assert p.preview.url.endswith(".jpg")
    assert p.thumbnail.url.endswith(".jpg")
    assert p.preview.storage.exists(p.preview.name)
    assert p.thumbnail.storage.exists(p.thumbnail.name)