# store/tests/conftest.py
import io, tempfile
from PIL import Image
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def sample_image():
    buf = io.BytesIO()
    Image.new("RGB", (200, 200), color="red").save(buf, format="JPEG")
    buf.seek(0)
    return SimpleUploadedFile("test.jpg", buf.read(), content_type="image/jpeg")