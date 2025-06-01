# cms/views.py

from django.shortcuts import render
from .models import HomeCarouselPhoto
from django.views.generic import (
    TemplateView,
)

class HomeView(TemplateView):
    template_name = "cms/home.html"
    def get_context_data(self, **kwargs):
        home_carousel_photo_list = HomeCarouselPhoto.objects.all().order_by('id')
        context = super(HomeView, self).get_context_data(**kwargs)
        context['home_carousel_photo_list'] = home_carousel_photo_list
        return context
