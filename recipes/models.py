# recipes/models.py
from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill, Transpose

def recipe_image_path(instance, filename):
    # folder per recipe; use tmp until PK assigned
    return f"recipes/{instance.pk or 'tmp'}/{filename}"

class Recipe(models.Model):
    title        = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be ≥ 2 characters")],
    )
    slug         = models.SlugField(max_length=220, unique=True)
    description  = models.TextField(blank=True)
    ingredients  = models.TextField(blank=True)
    instructions = models.TextField(blank=True)  # or RichTextField(blank=True)
    image        = models.ImageField(upload_to=recipe_image_path,
                                     blank=True, null=True)

    preview   = ImageSpecField(
        source='image',
        processors=[Transpose(), ResizeToFit(width=970, upscale=False)],
        format='JPEG',
        options={'quality': 70},
    )
    thumbnail = ImageSpecField(
        source='image',
        processors=[Transpose(), ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 60},
    )

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe_detail", kwargs={"slug": self.slug})
