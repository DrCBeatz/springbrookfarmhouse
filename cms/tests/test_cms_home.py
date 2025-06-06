# cms/tests/test_home_view.py
import pytest
from django.urls import reverse
from bs4 import BeautifulSoup

from cms.models import Testimonial, HomeCarouselPhoto


HOME_URL = reverse("home")


@pytest.mark.django_db
def test_home_status_ok(client):
    resp = client.get(HOME_URL)
    assert resp.status_code == 200
    assert resp.templates[0].name == "cms/home.html"


# ----------  carousel section ----------
@pytest.mark.django_db
def test_carousel_not_rendered_without_photos(client):
    resp = client.get(HOME_URL)
    assert b'class="swiper mySwiper"' not in resp.content


@pytest.mark.django_db
def test_carousel_renders_photos(client, sample_image):
    HomeCarouselPhoto.objects.create(title="Slide one", image=sample_image)
    resp = client.get(HOME_URL)

    soup = BeautifulSoup(resp.content, "html.parser")
    swiper = soup.select_one("div.swiper.mySwiper")
    assert swiper is not None
    assert swiper.select_one("img")["alt"] == "Slide one"


# ----------  testimonial section ----------
@pytest.mark.django_db
def test_testimonials_present(client):
    Testimonial.objects.create(name="Sara", location="Perth", text="Fantastic lamb")
    resp = client.get(HOME_URL)

    # Fast “string-contains” check
    assert b"Fantastic lamb" in resp.content

    # Optional stricter HTML assertion
    soup = BeautifulSoup(resp.content, "html.parser")
    txt = soup.find("blockquote").get_text(strip=True)
    assert "Fantastic lamb" in txt


@pytest.mark.django_db
def test_hidden_testimonials_not_shown(client):
    Testimonial.objects.create(
        name="Hidden", location="Nowhere", text="Invisible", display_on_homepage=False
    )
    resp = client.get(HOME_URL)
    assert b"Invisible" not in resp.content