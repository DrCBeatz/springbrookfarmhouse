# store/models.py
from django.db import models
from django.core.validators import MinLengthValidator,MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.conf import settings
from djrichtextfield.models import RichTextField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Transpose
from decimal import Decimal

ANCHOR = (
    ("c", "Centre"),
    ("t", "Top"),
    ("b", "Bottom"),
    ("l", "Left"),
    ("r", "Right"),
)

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
    
class Category(models.Model):
    title = models.CharField(
        max_length=200, unique=True,
        validators=[MinLengthValidator(2, "Title must be at least 2 characters")]
    )
    slug = models.SlugField(max_length=220, unique=True)
    is_taxable = models.BooleanField(default=False)
    producer_cut = models.DecimalField(
        max_digits=5, decimal_places=4, default=Decimal('0.85'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:category_detail', kwargs={'slug': self.slug})


class ProductType(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be at least 2 characters")]
    )
    slug = models.SlugField(max_length=220, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='product_types'
    )
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'category')  # same name in two different categories is OK
        ordering = ['title']

    def __str__(self):
        return f"{self.category.title} – {self.title}"

    def get_absolute_url(self):
        return reverse('store:product_type_detail',
                       kwargs={'category_slug': self.category.slug, 'slug': self.slug})
    
def product_image_path(instance, filename):
    # Falls back to “tmp” before PK exists on first save
    return f"products/{instance.pk or 'tmp'}/{filename}"


class Product(models.Model):
    # ————— core catalogue fields ————————————————
    title       = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be at least 2 characters")],
    )
    slug        = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)

    category     = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="products")
    producer     = models.ForeignKey(Producer, on_delete=models.PROTECT, related_name="products")

    # ————— pricing & inventory ————————————————
    price           = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price  = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    has_discount    = models.BooleanField(default=False)
    stock           = models.PositiveIntegerField(default=1)
    is_inventory_item = models.BooleanField(default=True)

    # ————— images ————————————————
    image     = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    thumbnail = ImageSpecField(
        source="image",
        processors=[Transpose(), ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 70},
    )
    preview   = ImageSpecField(
        source="image",
        processors=[Transpose(), ResizeToFit(width=970, upscale=False)],
        format="JPEG",
        options={"quality": 70},
    )
    anchor = models.CharField(max_length=1, choices=ANCHOR, default="c", blank=True)

    # ————— misc ————————————————
    featured_recipe       = models.ForeignKey(
        "recipes.Recipe", on_delete=models.SET_NULL, blank=True, null=True
    )
    eligible_for_delivery = models.BooleanField(default=False)
    enabled               = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ————— meta & constraints ————————————————
    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["slug"])]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="price_non_negative",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(discount_price__isnull=True)
                    | models.Q(discount_price__gt=0,
                               discount_price__lt=models.F("price"))
                ),
                name="discount_lt_price",
            ),
        ]

    # ————— convenience helpers ————————————————
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"slug": self.slug})

    @property
    def effective_price(self) -> Decimal:
        """Return the price the customer should see in the catalogue."""
        if self.has_discount and self.discount_price:
            return self.discount_price
        return self.price