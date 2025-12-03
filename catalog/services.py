from .models import Category, Product


class CatalogServices:

    @classmethod
    def get_category_products_list(cls, pk):
        """Class method for getting products list by category id"""

        category = Category.objects.get(id=pk)

        return Product.objects.filter(category=category)
