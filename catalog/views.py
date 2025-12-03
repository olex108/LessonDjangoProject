from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog.models import Category, ClientMessage, Contacts, Product

from .forms import ProductForm

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.utils.cache import get_cache_key

from .services import CatalogServices


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
        queryset = cache.get('products_list_queryset')
        if queryset is None:
            queryset = super().get_queryset()
            cache.set('products_list_queryset', queryset, 60*15)

        return queryset

        # return Product.objects.all().order_by("-created_at")


@method_decorator(cache_page(60 * 60), name='dispatch')
class ProductDetailView(DetailView):
    """CBV for render product detail page with GET request"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        """Add user to context data"""

        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        """
        POST method for product detail page with GET request from script in template
        If user has permission product publication boolean field change by opposite and save result
        Method return JSON Response with message
        """

        user = request.user
        if not user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden("У вас нет права отменять публикацию продукта")

        else:
            self.object = self.get_object()
            product = self.object

            product.is_publication = not product.is_publication
            product.save()

            status_message = "Продукт снят из публикации" if not product.is_publication else "Продукт опубликован"

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
        cache.delete('products_list_queryset')

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    CBV for update product page with GET request
    Have test function to compare user and product owner
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

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
            cache.delete('products_list_queryset')

        return product.owner == self.request.user or user.has_perm("catalog.delete_product")

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
        category_id = self.kwargs["pk"]
        queryset = CatalogServices.get_category_products_list(category_id)

        return queryset

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
