from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("products_list/", views.products_list, name="products_list"),
    path("product_info/<int:product_id>", views.product_info, name="product_info"),
    path("categories/", views.categories, name="categories"),
    path("contacts/", views.contacts, name="contacts"),
]
