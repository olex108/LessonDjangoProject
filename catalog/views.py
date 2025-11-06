from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Category, Contacts, ClientMessage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def home(request) -> HttpResponse:
    """Function to render the home page with GET request"""

    products = Product.objects.all()

    products_paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    page_obj = products_paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "catalog/home.html", context)


def products_list(request) -> HttpResponse:
    """Function to render all products list from database with GET request"""

    products = Product.objects.all()
    context = {
        "products": products,
    }

    return render(request, "catalog/products_list.html", context)


def product_info(request, product_id: int) -> HttpResponse:
    """
    Function to render all info of product by product_id with GET request

    product_id: Product ID
    """

    product = get_object_or_404(Product, id=product_id)

    context = {
        "product": product,
    }
    return render(request, "catalog/product_info.html", context)


def categories(request) -> HttpResponse:
    """Function to render all categories of products from database with GET request"""

    categories = Category.objects.all()

    context = {
        "categories": categories,
    }
    return render(request, "catalog/categories.html", context)


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

        contacts = Contacts.objects.get(id=1)

        context = super().get_context_data(**kwargs)
        context["contacts"] = contacts

        return context

    def form_valid(self, form):
        """Validate form, save in database and return JSON response by get AJAX-requested"""

        self.object = form.save()

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # return JSON response by get AJAX-requested
            return JsonResponse({"success": True})
        else:
            return super().form_valid(form)


def contacts(request) -> HttpResponse:
    """Function to render contact page wits GET and POST requests"""

    if request.method == "POST":

        name = request.POST["name"]
        phone = request.POST["phone"]
        message = request.POST["message"]

        ClientMessage.objects.create(name=name, phone=phone, message=message)

        return HttpResponse(f"Приветствую, {name}! Ваши данные успешно отправлены")

    elif request.method == "GET":

        contacts = Contacts.objects.get(id=1)

        context = {
            "contacts": contacts,
        }

        return render(request, "catalog/contacts.html", context)

    else:

        raise Http404
