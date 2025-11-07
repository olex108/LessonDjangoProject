from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("catalog/home/", views.HomeView.as_view(), name="home"),
    path("catalog/products_list/", views.ProductsListView.as_view(), name="products_list"),
    path("catalog/product_detail/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("catalog/categories/", views.CategoriesListView.as_view(), name="categories"),
    path("catalog/contacts/", views.ContactsView.as_view(), name="contacts"),
]
