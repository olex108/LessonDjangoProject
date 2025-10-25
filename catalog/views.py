from django.http import Http404, HttpResponse
from django.shortcuts import render


def home(request) -> HttpResponse:
    """Function to render the home page with GET request"""

    if request.method == "GET":

        return render(request, "catalog/home.html")

    else:

        raise Http404


def contacts(request) -> HttpResponse:
    """Function to render contact page wits GET and POST requests"""

    if request.method == "POST":

        name = request.POST["name"]
        phone = request.POST["phone"]
        message = request.POST["message"]

        return HttpResponse(f"Приветствую, {name}! Ваши данные успешно отправлены")

    elif request.method == "GET":

        return render(request, "catalog/contacts.html")

    else:

        raise Http404
