# blog/tests/test_views_template.py
import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from django.utils import timezone

LIST_URL   = reverse("blog:blog_post_list")
DETAIL_URL = lambda slug: reverse("blog:blog_post_detail", kwargs={"slug": slug})


@pytest.mark.django_db
def test_list_status_and_template(client, published_post):
    resp = client.get(LIST_URL)
    assert resp.status_code == 200
    assert "blog/blog_post_list.html" in [t.name for t in resp.templates]


@pytest.mark.django_db
def test_list_contains_post_card(client, published_post):
    resp  = client.get(LIST_URL)
    soup  = BeautifulSoup(resp.content, "html.parser")

    card  = soup.select_one("div.card")
    assert card is not None
    assert card.find("h5").text.strip() == "Published post"
    # href points to detail url
    assert card.find("a")["href"] == published_post.get_absolute_url()


@pytest.mark.django_db
def test_list_pagination(client, settings, author):
    settings.PAGE_SIZE = 6   # just to be explicit
    # create 10 posts
    for i in range(10):
        author.blog_posts.create(
            title=f"P{i}",
            slug=f"p-{i}",
            status="published",
            published_at=timezone.now() - timezone.timedelta(minutes=i),
        )
    resp = client.get(LIST_URL)
    soup = BeautifulSoup(resp.content, "html.parser")
    assert soup.select_one("ul.pagination") is not None


@pytest.mark.django_db
def test_detail_view_success(client, published_post):
    resp = client.get(DETAIL_URL("published-post"))
    assert resp.status_code == 200
    assert b"Published post" in resp.content
    assert b"<p>Hello world</p>" in resp.content   # content rendered


@pytest.mark.django_db
def test_detail_view_404_for_draft(client, draft_post):
    resp = client.get(DETAIL_URL("draft-post"))
    assert resp.status_code == 404