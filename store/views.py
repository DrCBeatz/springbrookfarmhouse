from django.views.generic import ListView, DetailView

from .models import Producer


class ProducerListView(ListView):
    model               = Producer
    template_name       = "store/producer_list.html"
    context_object_name = "producers"
    paginate_by         = 6

    def get_queryset(self):
        # only show active producers, alphabetical (defined in Meta.ordering)
        return Producer.objects.filter(is_active=True)


class ProducerDetailView(DetailView):
    model               = Producer
    template_name       = "store/producer_detail.html"
    context_object_name = "producer"

    def get_queryset(self):
        # keeps 404 behaviour if slug is inactive
        return Producer.objects.filter(is_active=True)