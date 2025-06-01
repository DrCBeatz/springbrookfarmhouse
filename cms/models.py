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