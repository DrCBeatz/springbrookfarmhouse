# store/tests/test_producer_views_template.py
import pytest
from django.urls import reverse

from store.models import Producer

# ---------- list view --------------------------------------------------------

@pytest.mark.django_db
def test_list_view_status_ok(client, producer_active):
    url = reverse("store:producer_list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert "store/producer_list.html" in [t.name for t in resp.templates]


@pytest.mark.django_db
def test_list_contains_only_active(client, producer_active, producer_inactive):
    resp = client.get(reverse("store:producer_list"))
    producers = list(resp.context["producers"])
    assert producers == [producer_active]                 # inactive filtered out
    assert producer_active.name in resp.content.decode()  # rendered to template
    assert producer_inactive.name not in resp.content.decode()


@pytest.mark.django_db
def test_list_pagination(client, six_active_producers):
    # With exactly 6 objects and paginate_by=6 we expect a single page.
    resp = client.get(reverse("store:producer_list"))
    assert resp.context["is_paginated"] is False
    assert resp.context["producers"].count() == 6


# ---------- detail view ------------------------------------------------------

@pytest.mark.django_db
def test_detail_view_ok(client, producer_active):
    url = reverse("store:producer_detail", kwargs={"slug": "spring-brook"})
    resp = client.get(url)
    assert resp.status_code == 200
    assert "store/producer_detail.html" in [t.name for t in resp.templates]
    # the producer’s name appears in the rendered HTML
    assert producer_active.name in resp.content.decode()


@pytest.mark.django_db
def test_detail_view_404_for_inactive(client, producer_inactive):
    url = reverse("store:producer_detail", kwargs={"slug": "hidden-farm"})
    resp = client.get(url)
    assert resp.status_code == 404