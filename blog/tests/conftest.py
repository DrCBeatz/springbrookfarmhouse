# blog/tests/conftest.py
import io, tempfile
from pathlib import Path

import pytest
from PIL import Image
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from blog.models import BlogPost


@pytest.fixture(scope="session")
def django_db_setup():
    # use a tmp MEDIA_ROOT so test images don’t pollute your dev media/
    tmp_media = tempfile.mkdtemp()
    settings.MEDIA_ROOT = tmp_media


@pytest.fixture
def author(db):
    return get_user_model().objects.create_user(
        username="writer", email="writer@example.com", password="pass"
    )


@pytest.fixture
def sample_image():
    buf = io.BytesIO()
    Image.new("RGB", (1200, 800), "green").save(buf, "JPEG")
    buf.seek(0)
    return SimpleUploadedFile("hero.jpg", buf.getvalue(), content_type="image/jpeg")


@pytest.fixture
def published_post(author, sample_image):
    post = BlogPost.objects.create(
        title="Published post",
        slug="published-post",
        author=author,
        content="<p>Hello world</p>",
        hero_image=sample_image,
        status=BlogPost.PUBLISHED,
        published_at=timezone.now(),
    )
    return post


@pytest.fixture
def draft_post(author):
    return BlogPost.objects.create(
        title="Draft post", slug="draft-post", author=author, status=BlogPost.DRAFT
    )