from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse

from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from catalog.models import Category, ClientMessage, Contacts, Product


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
        return Product.objects.all().order_by("-created_at")


class ProductDetailView(DetailView):
    """CBV for render product detail page with GET request"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class CategoriesListView(ListView):
    """CBV for render all categories list from database with GET request"""

    model = Category
    template_name = "catalog/categories_list.html"
    context_object_name = "categories"


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
            contacts = Contacts.objects.get(id=1)
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
