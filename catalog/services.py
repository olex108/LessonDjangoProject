from django.core.cache import cache

from .models import Category, Product


class CatalogServices:

    @classmethod
    def get_category_products_list(cls, pk):
        """Class method for getting products list by category id"""

        category = Category.objects.get(id=pk)

        return Product.objects.filter(category=category)


class CatalogCacheServices:

    @classmethod
    def get_products_list_from_cache(cls):
        """Class method for getting and cache products list"""

        queryset = cache.get("products_list_queryset")
        if queryset is None:
            queryset = Product.objects.all().order_by("-created_at")
            cache.set("products_list_queryset", queryset, 60 * 60 * 1)

        return queryset
