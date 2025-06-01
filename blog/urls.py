# blog/urls.py
from django.urls import path
from .views import BlogPostListView, BlogPostDetailView

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="blog_post_list"),
    path("<slug:slug>/", BlogPostDetailView.as_view(), name="blog_post_detail"),
]