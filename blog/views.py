# blog/views.py
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blog_post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        # show published posts only, newest first
        return (
            BlogPost.objects.filter(status=BlogPost.PUBLISHED,
                                    published_at__lte=timezone.now())
            .select_related("author")
            .prefetch_related("photos")
        )


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return (
            BlogPost.objects.filter(status=BlogPost.PUBLISHED)
            .select_related("author")
            .prefetch_related("photos")
        )