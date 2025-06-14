# Generated by Django 5.2.1 on 2025-06-01 19:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeCarouselPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Title must be ≥ 2 characters')])),
                ('image', models.ImageField(upload_to='carousel/')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Lower = shown first')),
                ('alt_text', models.CharField(blank=True, help_text='Image alt text', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'carousel photo',
                'verbose_name_plural': 'carousel photos',
                'ordering': ['order', 'id'],
            },
        ),
    ]
