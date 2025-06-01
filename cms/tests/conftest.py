# cms/tests/conftest.py
import io
import tempfile
from pathlib import Path

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    """Tell pytest-django to use the real settings but a tmp MEDIA_ROOT."""
    tmp_media = tempfile.mkdtemp()
    settings.MEDIA_ROOT = tmp_media


@pytest.fixture
def sample_image() -> SimpleUploadedFile:
    """Generate an in-memory 100×100 JPEG for uploads."""
    buffer = io.BytesIO()
    Image.new("RGB", (100, 100), color="red").save(buffer, "JPEG")
    buffer.seek(0)
    return SimpleUploadedFile(
        name="test.jpg",
        content=buffer.getvalue(),
        content_type="image/jpeg",
    )