from django.core.management import call_command
from django.core.management.base import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    help = "Add products to the database"

    def handle(self, *args, **kwargs) -> None:
        """
        Method to delete and add posts to the database
        """

        # Удаляем существующие записи
        Post.objects.all().delete()

        call_command("loaddata", "db_fixtures/posts_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
