from django.db import models

from users.models import User


class Post(models.Model):
    """
    Model representing a blog post, for save contacts of client, save message and field is_answered to keep
    """

    DRAFT = "DRAFT"
    PUBLISH = "PUBLISH"
    SUBMIT = "SUBMIT"

    PUBLISH_STATUS_CHOICES = [
        (DRAFT, "Черновик"),
        (PUBLISH, "Публикуется"),
        (SUBMIT, "На рассмотрение"),
    ]

    title = models.CharField(max_length=150, verbose_name="Заголовок", help_text="заголовок")
    content = models.TextField(verbose_name="Содержимое", help_text="содержимое")
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    publish_status = models.CharField(
        default=DRAFT, max_length=15, choices=PUBLISH_STATUS_CHOICES, verbose_name="Подача на публикацию"
    )
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    views_counter = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return f"{self.title} - {self.created_at} - {self.views_counter}"

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = ["-created_at"]

        permissions = [
            ("can_publish_post", "Can publish post"),
        ]
