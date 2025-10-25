from django.db import models
from django.db.models import CharField


class Category(models.Model):
    """
    Model representing a category
    Model has field id with is not indicated witch is primary key for model
    and ForeignKey for model Product
    """

    name = models.CharField(max_length=100, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']


class Product(models.Model):
    """
    Model representing a product
    """

    name = models.CharField(max_length=100, verbose_name="Продукт")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="images/", verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.FloatField(verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['name']
