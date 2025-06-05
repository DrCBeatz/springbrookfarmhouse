# recipes/tests/test_views_template.py
import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from recipes.models import Recipe
from django.utils.html import escape



LIST_URL   = reverse("recipes:recipe_list")
DETAIL_URL = lambda slug: reverse("recipes:recipe_detail", kwargs={"slug": slug})


# ---------- list view ----------
@pytest.mark.django_db
def test_list_view_ok(client, recipe):
    resp = client.get(LIST_URL)
    assert resp.status_code == 200
    assert "recipes/recipe_list.html" in [t.name for t in resp.templates]


@pytest.mark.django_db
def test_list_contains_card(client, recipe):
    resp = client.get(LIST_URL)
    soup = BeautifulSoup(resp.content, "html.parser")
    card = soup.select_one("div.card")
    assert card is not None
    assert card.find("h5").text.strip() == "Chocolate Cake"
    assert card.find("a")["href"] == recipe.get_absolute_url()


@pytest.mark.django_db
def test_list_pagination(client):
    for i in range(8):  # > paginate_by (6)
        Recipe.objects.create(title=f"R{i}", slug=f"r-{i}")
    resp = client.get(LIST_URL)
    soup = BeautifulSoup(resp.content, "html.parser")
    assert soup.select_one("ul.pagination") is not None


# ---------- detail view ----------
@pytest.mark.django_db
def test_detail_view_ok(client, recipe):
    resp = client.get(DETAIL_URL("chocolate-cake"))
    assert resp.status_code == 200
    
    escaped = escape("Rich & moist.")
    assert f"<p>{escaped}</p>".encode() in resp.content

@pytest.mark.django_db
def test_detail_404(client):
    resp = client.get(DETAIL_URL("does-not-exist"))
    assert resp.status_code == 404