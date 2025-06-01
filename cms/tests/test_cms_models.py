# cms/tests/test_models.py
import pytest
from cms.models import HomeCarouselPhoto
from pathlib import Path


@pytest.mark.django_db
def test_str(sample_image):
    obj = HomeCarouselPhoto.objects.create(title="Slide 1", image=sample_image)
    assert str(obj) == "Slide 1"


@pytest.mark.django_db
def test_default_ordering(sample_image):
    HomeCarouselPhoto.objects.create(title="B", image=sample_image, order=2)
    HomeCarouselPhoto.objects.create(title="A", image=sample_image, order=1)

    titles = list(HomeCarouselPhoto.objects.values_list("title", flat=True))
    assert titles == ["A", "B"] # ordered by .order then pk


@pytest.mark.django_db
def test_image_specs_exist(sample_image, settings):
    obj = HomeCarouselPhoto.objects.create(title="Photo", image=sample_image)
    obj.hero.generate()
    assert obj.hero.url.endswith(".jpg")
    # ask storage whether the object exists (works for local FS or S3)
    assert obj.hero.storage.exists(obj.hero.name)