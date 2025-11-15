from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Model of user"""

    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = PhoneNumberField(blank=True, verbose_name="Телефон")
    country = models.CharField(max_length=30, verbose_name="Страна", help_text="страна")
    avatar = models.ImageField(upload_to="users/avatar/", verbose_name="Аватар", help_text="Загрузите аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
