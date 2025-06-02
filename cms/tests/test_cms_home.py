# cms/tests/test_home_view.py
import pytest
from django.urls import reverse
from cms.models import HomeCarouselPhoto
from bs4 import BeautifulSoup   # add “beautifulsoup4” to dev deps

HOME_URL = reverse("home")


@pytest.mark.django_db
def test_home_200(client):
    resp = client.get(HOME_URL)
    assert resp.status_code == 200
    assert b"Spring Brook Farmhouse" in resp.content


@pytest.mark.django_db
def test_carousel_absent_when_no_images(client):
    resp = client.get(HOME_URL)
    assert b'class="swiper mySwiper"' not in resp.content   # guard-rail works


@pytest.mark.django_db
def test_carousel_present_and_images_rendered(client, sample_image):
    # set-up one slide
    photo = HomeCarouselPhoto.objects.create(title="Slide", image=sample_image)

    resp = client.get(HOME_URL)
    assert resp.status_code == 200
    soup = BeautifulSoup(resp.content, "html.parser")

    # Swiper root exists
    swiper = soup.select_one("div.swiper.mySwiper")
    assert swiper is not None

    # Our image url is in the markup
    img_tags = [img["src"] for img in swiper.select("img")]
    assert photo.hero.url in img_tags

    # alt text fallback logic
    assert soup.find("img")["alt"] == "Slide"