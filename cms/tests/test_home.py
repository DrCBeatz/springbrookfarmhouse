# cms/tests/test_home.py
import pytest
from django.urls import reverse

@pytest.mark.django_db(False)
def test_home_status_code(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db(False)
def test_home_template_used(client):
    url = reverse('home')
    response = client.get(url)
    templates = [t.name for t in response.templates]
    assert "cms/home.html" in templates

@pytest.mark.django_db(False)
def test_home_containtes_expected_text(client):
    url = reverse('home')
    response = client.get(url)
    assert b"Welcome to Spring Brook Farmhouse" in response.content