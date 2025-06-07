# store/models.py
from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.conf import settings
from djrichtextfield.models import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Transpose


def producer_image_path(instance, filename):
    # Falls back to “tmp” before PK exists on first save
    return f"producers/{instance.pk or 'tmp'}/{filename}"


class Producer(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    slug = models.SlugField(max_length=220, unique=True)

    description = models.CharField(max_length=400, blank=True)
    content = RichTextField(blank=True)

    image = models.ImageField(
        upload_to=producer_image_path, blank=True, null=True
    )
    preview = ImageSpecField(
        source='image',
        processors=[Transpose(), ResizeToFit(width=970, upscale=False)],
        format='JPEG',
        options={'quality': 70},
    )
    thumbnail = ImageSpecField(
        source='image',
        processors=[Transpose(), ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 70},
    )

    # links
    video_url = models.URLField(max_length=300, blank=True)
    website_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'producer'
        verbose_name_plural = 'producers'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:producer_detail', kwargs={'slug': self.slug})