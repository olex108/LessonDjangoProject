from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("blogs/posts/", views.PostsListView.as_view(), name="posts_list"),
    path("blogs/posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("blogs/posts/new", views.PostCreateView.as_view(), name="post_create"),
    path("blogs/<int:pk>/post_update/", views.PostUpdateView.as_view(), name="post_update"),
    path("blogs/<int:pk>/post_delete/", views.PostDeleteView.as_view(), name="post_delete"),
]
