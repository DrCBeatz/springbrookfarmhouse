# blog/models.py
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinLengthValidator

from djrichtextfield.models import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill, Transpose
from django.utils import timezone

def post_image_path(instance, filename):
    # e.g. "blog/42/hero.jpg"
    return f"blog/{instance.pk}/{filename}"


class BlogPost(models.Model):
    DRAFT   = "draft"
    PUBLISHED = "published"

    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
    ]

    title       = models.CharField(
                    max_length=200,
                    validators=[MinLengthValidator(2, "Title must be ≥ 2 characters")],
                  )
    slug        = models.SlugField(unique=True, max_length=220)
    author      = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name="blog_posts",
                  )
    caption     = models.CharField(max_length=400, blank=True)
    hero_image  = models.ImageField(upload_to=post_image_path, blank=True)
    hero_preview = ImageSpecField(
                    source="hero_image",
                    processors=[Transpose(), ResizeToFit(width=600, upscale=False)],
                    format="JPEG",
                    options={"quality": 75},
                  )
    video_link  = models.URLField(max_length=300, blank=True)
    content     = RichTextField(blank=True)
    status      = models.CharField(
                    max_length=9, choices=STATUS_CHOICES, default=DRAFT
                  )
    published_at = models.DateTimeField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes  = [models.Index(fields=["status", "published_at"])]

    def __str__(self):
        return self.title

    # convenient helpers
    def publish(self):
        self.status = self.PUBLISHED
        if not self.published_at:
            self.published_at = timezone.now()
        self.save(update_fields=["status", "published_at"])

    def get_absolute_url(self):
        return reverse("blog:blog_post_detail", kwargs={"slug": self.slug})


def post_photo_path(instance, filename):
    # e.g. "blog/42/photos/slide_1.jpg"
    return f"blog/{instance.post_id}/photos/{filename}"


class BlogPostPhoto(models.Model):
    post        = models.ForeignKey(
                    BlogPost,
                    on_delete=models.CASCADE,
                    related_name="photos",
                  )
    title       = models.CharField(max_length=200, blank=True)
    image       = models.ImageField(upload_to=post_photo_path)
    preview     = ImageSpecField(
                    source="image",
                    processors=[Transpose(), ResizeToFit(width=970, upscale=False)],
                    format="JPEG",
                    options={"quality": 75},
                  )
    thumbnail   = ImageSpecField(
                    source="image",
                    processors=[Transpose(), ResizeToFill(200, 200)],
                    format="JPEG",
                    options={"quality": 70},
                  )
    alt_text    = models.CharField(max_length=255, blank=True)
    order       = models.PositiveSmallIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or f"Photo {self.pk}"