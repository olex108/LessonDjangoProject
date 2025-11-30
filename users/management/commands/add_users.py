from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user1 = User.objects.create(email="test@test.com")
        user1.set_password("1234qwer")
        user1.is_active = True
        user1.is_staff = False
        user1.is_superuser = False
        user1.save()

        user2 = User.objects.create(email="test1@test.com")
        user2.set_password("1234qwer")
        user2.is_active = True
        user2.is_staff = False
        user2.is_superuser = False
        user2.save()

        user3 = User.objects.create(email="test2@test.com")
        user3.set_password("1234qwer")
        user3.is_active = True
        user3.is_staff = False
        user3.is_superuser = False
        user3.save()
