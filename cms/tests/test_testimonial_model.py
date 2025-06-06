# cms/tests/test_testimonial_model.py
import pytest
from django.utils import timezone
from cms.models import Testimonial


@pytest.mark.django_db
def test_str_readable():
    t = Testimonial.objects.create(name="Alice", location="Perth", text="Great beef")
    assert str(t) == "Alice – Perth"          # __str__ formatting


@pytest.mark.django_db
def test_blank_location_fallback():
    t = Testimonial.objects.create(name="Bob", location="", text="Yummy!")
    assert str(t).endswith("Unknown location")


@pytest.mark.django_db
def test_default_display_flag_true():
    t = Testimonial.objects.create(name="Alice", location="Perth", text="Great beef")
    assert t.display_on_homepage is True


@pytest.mark.django_db
def test_ordering_desc_created_at():
    older = Testimonial.objects.create(
        name="Old", location="Ottawa", text="Older", created_at=timezone.now()
    )
    newer = Testimonial.objects.create(
        name="New", location="Ottawa", text="Newer", created_at=timezone.now()
    )
    # queryset order defined in Meta.ordering
    assert list(Testimonial.objects.all()) == [newer, older]