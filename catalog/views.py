from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog.models import Category, ClientMessage, Contacts, Product

from .forms import ProductForm
from .services import CatalogCacheServices, CatalogServices


class HomeView(ListView):
    """CBV for render home page with pagination of products"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")


class ProductsListView(ListView):
    """CBV for render all products list from database with GET request"""

    model = Product
    template_name = "catalog/products_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return CatalogCacheServices.get_products_list_from_cache()


class ProductDetailView(DetailView):
    """CBV for render product detail page with GET request"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        """
        Update method to cache page HTML response
        To correct cache for different users (user, owner, moderator, moderator&owner) page can be cached with
        different cache keys
        """

        self.cache_key = f"product_detail:{kwargs['pk']}"

        if request.method == "GET":

            if self.request.user.is_authenticated:
                # If user is_authenticated, chek "can_unpublish_product" permissions and add ":moderator" to cache key
                if self.request.user.has_perm("catalog.can_unpublish_product"):
                    self.cache_key += ":moderator"
                # Try to get cached_response with user id in "cache_key" and if it exists add :owner:# to cache key
                if self.request.user.id == self.get_object().owner.id:
                    self.cache_key += f":owner:{self.request.user.id}"

            cached_response = cache.get(self.cache_key)

            if cached_response:
                return cached_response

        response = super().dispatch(request, *args, **kwargs)

        if request.method == "GET" and response.status_code == 200:

            try:
                # Render response before set cache
                response.render()
                cache.set(self.cache_key, response, 60 * 3)
                print(f"[{self.cache_key}] Сохранено в кэш")
            except Exception as e:
                print(f"Ошибка при кэшировании: {e}")

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden("У вас нет права отменять публикацию продукта")
        else:
            self.object = self.get_object()
            product = self.object

            product.is_publication = not product.is_publication
            product.save()

            status_message = "Продукт снят из публикации" if not product.is_publication else "Продукт опубликован"

            # Delete caches of product page after change with POST
            for cache_key in [
                f"product_detail:{kwargs['pk']}",
                f"product_detail:{kwargs['pk']}:owner:{self.object.owner.id}",
                f"product_detail:{kwargs['pk']}:moderator",
                f"product_detail:{kwargs['pk']}:moderator:owner:{self.object.owner.id}",
            ]:
                cache.delete(cache_key)
                print(f"[{cache_key}] Удален из кэша после POST запроса")

            return JsonResponse({"status": "success", "message": status_message, "new_state": product.is_publication})


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV for create product page with GET request"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        """Add user id to Product field owner"""

        form.instance.owner = self.request.user
        # Delete from cache
        cache.delete("products_list_queryset")

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    CBV for update product page with GET request
    Have test function to compare user and product owner
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        """Update method to delete page cache"""

        response = super().form_valid(form)
        product_id = self.object.pk

        # Delete caches of product page after change with POST
        for cache_key in [
            f"product_detail:{product_id}",
            f"product_detail:{product_id}:owner:{self.object.owner.id}",
            f"product_detail:{product_id}:moderator",
            f"product_detail:{product_id}:moderator:owner:{self.object.owner.id}",
        ]:
            cache.delete(cache_key)
            print(f"[{cache_key}] Удален из кэша после POST запроса")

        return response

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

    def handle_no_permission(self):
        return redirect("catalog:product_detail", pk=self.kwargs["pk"])


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """CBV for delete product page with GET request"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products_list")

    def test_func(self):
        user = self.request.user
        product = self.get_object()
        is_has_perm = product.owner == self.request.user or user.has_perm("catalog.delete_product")
        # Delete from cache
        if is_has_perm:
            cache.delete("products_list_queryset")

        return is_has_perm

    def handle_no_permission(self):
        return redirect("catalog:product_detail", pk=self.kwargs["pk"])


class CategoriesListView(ListView):
    """CBV for render all categories list from database with GET request"""

    model = Category
    template_name = "catalog/categories_list.html"
    context_object_name = "categories"


class CategoryProductsListView(ListView):
    """CBV for render all products list from database with GET request"""

    model = Product
    template_name = "catalog/category_products_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return CatalogServices.get_category_products_list(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(id=self.kwargs["pk"])

        return context


class ContactsView(CreateView):
    """
    Class to render contact information about company and form to fill user contacts and message
    Class use model ClientMessage to create form, and use method get_context_data() to add information about company

    Class use form_valid to create JSON request about success feel of form and save in database
    """

    model = ClientMessage
    fields = ["name", "phone", "message"]
    template_name = "catalog/contacts_form.html"
    success_url = reverse_lazy("catalog:contacts")

    def get_context_data(self, **kwargs):
        """Add Contacts to context data"""

        try:
            contacts = Contacts.objects.get()
        except ObjectDoesNotExist:
            return super().get_context_data(**kwargs)

        context = super().get_context_data(**kwargs)
        context["contacts"] = contacts

        return context

    def form_valid(self, form):
        """Validate form, save in database and return JSON response by get AJAX-requested"""

        self.object = form.save()

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            # return JSON response by get AJAX-requested
            return JsonResponse({"success": True})
        else:
            return super().form_valid(form)
