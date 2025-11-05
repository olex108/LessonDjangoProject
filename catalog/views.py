from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Category, Contacts, ClientMessage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
