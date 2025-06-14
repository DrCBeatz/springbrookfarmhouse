# core/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
    path('', include(("store.urls", "store"), namespace="store")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("recipes/", include("recipes.urls", namespace="recipes")),
    path('djrichtextfield/', include('djrichtextfield.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
