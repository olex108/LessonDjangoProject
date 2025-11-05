from django.db import models


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
        ordering = ["name"]


class Product(models.Model):
    """
    Model representing a product with fields

    id: pk of product
    name: name
    description: details about product
    image: path to image file
    category: ForeignKey of Category
    price: price
    created_at: date time info about creation of product
    updated_at: lust update of product
    """

    name = models.CharField(max_length=100, verbose_name="Продукт")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="images/", verbose_name="Изображение", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.FloatField(verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]


class Contacts(models.Model):
    """
    Model representing a contacts of company with fields

    id: pk of contact
    name: name
    email: email
    phone: phone number
    """

    name = models.CharField(max_length=100, verbose_name="Название компании")
    email = models.EmailField(verbose_name="Почта")
    phone = models.CharField(max_length=10, verbose_name="Телефон")

    def __str__(self) -> str:
        return f"{self.name} - {self.email} - {self.phone}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class ClientMessage(models.Model):

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=12, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Отправлено")
    is_answered = models.BooleanField(default=False, verbose_name="Отвечено")

    def __str__(self) -> str:
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["created_at"]


