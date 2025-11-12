from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Post
from .forms import PostForm


class PostsListView(ListView):
    """CBV for render posts list view"""

    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.all().filter(is_published=True)
        return queryset


class PostDetailView(DetailView):
    """CBV for render post detail view"""

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    """CBV for create post view"""

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        # Используем reverse_lazy, чтобы получить URL с подставленным id
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class PostUpdateView(UpdateView):
    """CBV for update post view"""

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        # Используем reverse_lazy, чтобы получить URL с подставленным id
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(DeleteView):
    """CBV for delete post view"""

    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:posts_list")
