# cms/views.py

from django.shortcuts import render
from .models import HomeCarouselPhoto, Testimonial
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "cms/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["home_carousel_photo_list"] = HomeCarouselPhoto.objects.all().order_by("id")
        context["testimonials"] = (
            Testimonial.objects.filter(display_on_homepage=True)
            .order_by("created_at")
        )
        return context