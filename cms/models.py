# cms/models.py
from django.db import models
from django.core.validators import MinLengthValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Transpose


class HomeCarouselPhoto(models.Model):
    title       = models.CharField(
                    max_length=200,
                    validators=[MinLengthValidator(2, "Title must be ≥ 2 characters")]
                )
    image       = models.ImageField(upload_to="carousel/")
    preview     = ImageSpecField(
                    source='image',
                    processors=[Transpose(), ResizeToFit(width=970, upscale=False)],
                    format='JPEG',
                    options={'quality': 70},
                )
    hero        = ImageSpecField(
                    source='image',
                    processors=[Transpose(), ResizeToFit(width=1600, upscale=False)],
                    format='JPEG',
                    options={'quality': 85},
                )
    thumbnail   = ImageSpecField(
                    source='image',
                    processors=[Transpose(), ResizeToFill(200, 200)],
                    format='JPEG',
                    options={'quality': 70},
                 )
    order       = models.PositiveSmallIntegerField(default=0, help_text="Lower = shown first")
    alt_text    = models.CharField(max_length=255, blank=True, help_text="Image alt text")

    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "carousel photo"
        verbose_name_plural = "carousel photos"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2, "Name must be ≥ 2 characters")]
    )
    location = models.CharField(max_length=120, blank=True)
    text = models.TextField()

    image = models.ImageField(
        upload_to="testimonials/",
        null=True,
        blank=True
    )
    preview = ImageSpecField(
        source="image",
        id="cms:image:testimonial_preview",
        processors=[Transpose(), ResizeToFit(width=200, upscale=False)],
        format="JPEG",
        options={"quality": 70},
    )

    display_on_homepage = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} – {self.location or 'Unknown location'}"