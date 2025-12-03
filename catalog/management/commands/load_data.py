import os

from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.core.management.base import BaseCommand

from blog.models import Post
from catalog.models import Category, Product
from users.models import User


class Command(BaseCommand):
    help = "Add products to the database"

    def handle(self, *args, **kwargs) -> None:
        """
        Method to delete and add superusers, users, groups, data to catalog and blog apps
        """

        # Delete data
        Product.objects.all().delete()
        Category.objects.all().delete()
        Post.objects.all().delete()

        User.objects.all().delete()
        Group.objects.all().delete()

        # Create superuser with email address with send mails
        superuser1 = User.objects.create(email=os.getenv("EMAIL_ADDRESS"), id=4)
        superuser1.set_password("1234qwer")
        superuser1.is_active = True
        superuser1.is_staff = True
        superuser1.is_superuser = True
        superuser1.save()

        superuser2 = User.objects.create(email="superuser@test.com", id=5)
        superuser2.set_password("1234qwer")
        superuser2.is_active = True
        superuser2.is_staff = True
        superuser2.is_superuser = True
        superuser2.save()

        # Permissions
        # Product permissions
        add_product = Permission.objects.get(codename="add_product")
        change_product = Permission.objects.get(codename="change_product")
        delete_product = Permission.objects.get(codename="delete_product")
        view_product = Permission.objects.get(codename="view_product")
        can_unpublish_product = Permission.objects.get(codename="can_unpublish_product")
        # Post permissions
        add_post = Permission.objects.get(codename="add_post")
        change_post = Permission.objects.get(codename="change_post")
        delete_post = Permission.objects.get(codename="delete_post")
        view_post = Permission.objects.get(codename="view_post")
        can_publish_post = Permission.objects.get(codename="can_publish_post")

        # Create groups
        user_group = Group.objects.create(name="Пользователь")
        user_group.save()
        user_group.permissions.clear()
        user_group.permissions.add(add_product, change_product, view_product, add_post, change_post, view_post)

        moderator_product_group = Group.objects.create(name="Модератор продуктов")
        moderator_product_group.save()
        moderator_product_group.permissions.clear()
        moderator_product_group.permissions.add(add_product, delete_product, view_product, can_unpublish_product)
        moderator_product_group.save()

        moderator_post_group = Group.objects.create(name="Контент-менеджер")
        moderator_post_group.save()
        moderator_post_group.permissions.clear()
        moderator_post_group.permissions.add(add_post, delete_post, view_post, can_publish_post)
        moderator_post_group.save()

        # Create users
        user_1 = User.objects.create(email="user_1@test.com", id=1)
        user_1.set_password("1234qwer")
        user_1.is_active = True
        user_1.is_staff = False
        user_1.is_superuser = False
        user_1.save()

        user_2 = User.objects.create(email="user_2@test.com", id=2)
        user_2.set_password("1234qwer")
        user_2.is_active = True
        user_2.is_staff = False
        user_2.is_superuser = False
        user_2.save()

        user_3 = User.objects.create(email="user_3@test.com", id=3)
        user_3.set_password("1234qwer")
        user_3.is_active = True
        user_3.is_staff = False
        user_3.is_superuser = False
        user_3.save()

        # Add users into groups
        user_1.groups.add(user_group)
        user_2.groups.add(user_group)
        user_3.groups.add(user_group)
        user_1.groups.add(moderator_product_group)
        user_2.groups.add(moderator_post_group)

        # Load data from fixtures
        call_command("loaddata", "db_fixtures/categories_fixture.json")
        call_command("loaddata", "db_fixtures/products_fixture.json")
        call_command("loaddata", "db_fixtures/posts_fixture.json")

        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
