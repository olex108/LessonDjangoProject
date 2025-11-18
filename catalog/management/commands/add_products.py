from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add products to the database"

    def handle(self, *args, **kwargs) -> None:
        """
        Method to delete and add products and categories to the database
        """

        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "db_fixtures/categories_fixture.json")
        call_command("loaddata", "db_fixtures/products_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
