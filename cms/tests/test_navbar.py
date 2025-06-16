# cms/tests/test_navbar.py

import pytest
from django.urls import reverse
from bs4 import BeautifulSoup

HOME_URL = reverse("home")
A_LINK = "https://www.airbnb.ca/rooms/1426993368785918604"


@pytest.mark.django_db
def test_navbar_has_airbnb_link(client):
    response = client.get(HOME_URL)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    link = soup.select_one(f'a[href="{A_LINK}"]')

    # 1️⃣ The link exists
    assert link is not None, "AirBnB link disappeared from the navbar"

    # 2️⃣ The visible text is correct
    assert link.get_text(strip=True) == "Book AirBnB"

    # 3️⃣ It still opens in a new tab
    assert link["target"] == "_blank"