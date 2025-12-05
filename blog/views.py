import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from src.mailing import send_email_100_views

from .forms import PostForm
from .models import Post


class PostsListView(ListView):
    """CBV for render posts list view"""

    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.all().order_by("-views_counter")
        return queryset


class PostDetailView(DetailView):
    """CBV for render post detail view"""

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Add user to context data"""

        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        # Send email if post get 100 views
        if self.object.views_counter == 100:
            send_email_100_views(os.getenv("EMAIL_ADDRESS"), self.object.title)

        return self.object


class PostCreateView(LoginRequiredMixin, CreateView):
    """CBV for create post view"""

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        # Используем reverse_lazy, чтобы получить URL с подставленным id
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        """Add author to post form"""

        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Add user to form kwargs. Fou using in field 'publish_status'
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """CBV for update post view"""

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        # Используем reverse_lazy, чтобы получить URL с подставленным id
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        """
        Add user to form kwargs. Fou using in field 'publish_status'
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user

        return kwargs

    def form_valid(self, form):
        """Add author to post form"""
        print(form.instance.publish_status)

        if form.instance.publish_status == "PUBLISH":
            form.instance.is_published = True
        else:
            form.instance.is_published = False

        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """CBV for delete post view"""

    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:posts_list")

    def test_func(self):
        user = self.request.user
        post = self.get_object()
        return post.author == self.request.user or user.has_perm("blog.can_publish_post")

    def handle_no_permission(self):
        return redirect("blog:post_detail", pk=self.kwargs["pk"])
