# blog/tests/test_models.py
import pytest
from django.urls import reverse
from django.utils import timezone
from blog.models import BlogPost


@pytest.mark.django_db
def test_str(author):
    post = BlogPost.objects.create(title="My title", slug="my-title", author=author)
    assert str(post) == "My title"


@pytest.mark.django_db
def test_publish_helper(author):
    post = BlogPost.objects.create(title="Draft", slug="draft", author=author)
    assert post.status == BlogPost.DRAFT
    assert post.published_at is None

    post.publish()
    assert post.status == BlogPost.PUBLISHED
    assert post.published_at is not None
    assert abs(post.published_at - timezone.now()).seconds < 5


@pytest.mark.django_db
def test_ordering(published_post, author):
    older = BlogPost.objects.create(
        title="Older", slug="older", author=author, status=BlogPost.PUBLISHED,
        published_at=timezone.now() - timezone.timedelta(days=1)
    )
    titles = list(BlogPost.objects.filter(status=BlogPost.PUBLISHED).values_list("title", flat=True))
    assert titles == ["Published post", "Older"]   # newest first


@pytest.mark.django_db
def test_get_absolute_url(published_post):
    assert published_post.get_absolute_url() == reverse(
        "blog:blog_post_detail", kwargs={"slug": "published-post"}
    )