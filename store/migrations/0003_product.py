# Generated by Django 5.2.1 on 2025-06-08 19:42

import django.core.validators
import django.db.models.deletion
import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
        ('store', '0002_category_producttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Title must be at least 2 characters')])),
                ('slug', models.SlugField(max_length=220, unique=True)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)])),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('has_discount', models.BooleanField(default=False)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('is_inventory_item', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=store.models.product_image_path)),
                ('anchor', models.CharField(blank=True, choices=[('c', 'Centre'), ('t', 'Top'), ('b', 'Bottom'), ('l', 'Left'), ('r', 'Right')], default='c', max_length=1)),
                ('eligible_for_delivery', models.BooleanField(default=False)),
                ('enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.category')),
                ('featured_recipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.recipe')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.producer')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.producttype')),
            ],
            options={
                'ordering': ['title'],
                'indexes': [models.Index(fields=['slug'], name='store_produ_slug_361302_idx')],
                'constraints': [models.CheckConstraint(condition=models.Q(('price__gte', 0)), name='price_non_negative'), models.CheckConstraint(condition=models.Q(('discount_price__isnull', True), models.Q(('discount_price__gt', 0), ('discount_price__lt', models.F('price'))), _connector='OR'), name='discount_lt_price')],
            },
        ),
    ]
