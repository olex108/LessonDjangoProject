from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("catalog/home/", views.HomeView.as_view(), name="home"),
    path("catalog/products/", views.ProductsListView.as_view(), name="products_list"),
    path("catalog/products/new", views.ProductCreateView.as_view(), name="product_create"),
    path("catalog/products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("catalog/products/<int:pk>/update", views.ProductUpdateView.as_view(), name="product_update"),
    path("catalog/products/<int:pk>/delete", views.ProductDeleteView.as_view(), name="product_delete"),
    path("catalog/categories/", views.CategoriesListView.as_view(), name="categories"),
    path("catalog/contacts/", views.ContactsView.as_view(), name="contacts"),
]
