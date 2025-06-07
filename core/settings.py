# core/settings.py

import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for production
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Debug mode
DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = ["*"]

TINYMCE_KEY = env.str("TINYMCE_KEY", default="")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'django_cleanup.apps.CleanupConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'imagekit',
    'djrichtextfield',
    # Local
    "core",
    "accounts.apps.AccountsConfig",
    "cms.apps.CmsConfig",
    "blog.apps.BlogConfig",
    "recipes.apps.RecipesConfig",
    "store.apps.StoreConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'core.wsgi.application'

# Database configuration
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB", "django_test"),
        "USER": env.str("POSTGRES_USER", "django"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", "django"),
        "HOST": POSTGRES_HOST,
        "PORT": "5432",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DJRICHTEXTFIELD_CONFIG = {
    'js': ['//cdn.tiny.cloud/1/' + TINYMCE_KEY + '/tinymce/5/tinymce.min.js'],
    'init_template': 'djrichtextfield/init/tinymce.js',
    'settings': {
        'menubar': False,
        'plugins': 'link image',
        'toolbar': 'undo redo | styleselect | forecolor | bold italic | alignleft aligncenter alignright | link image | removeformat ',
        'width': 800
    }
}

AUTH_USER_MODEL = "accounts.CustomUser"

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True


# Static files & Media files

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_OBJECT_PARAMETERS = { "CacheControl": "max-age=86400" }
    AWS_QUERYSTRING_AUTH = False