from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("products_list/", views.ProductsListView.as_view(), name="products_list"),
    path("product_detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("categories/", views.CategoriesListView.as_view(), name="categories"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
]
