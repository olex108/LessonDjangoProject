from django.db import models


class Post(models.Model):
    """
    Model representing a blog post, for save contacts of client, save message and field is_answered to keep
    """

    title = models.CharField(max_length=150, verbose_name="Заголовок", help_text="заголовок")
    content = models.TextField(verbose_name="Содержимое", help_text="содержимое")
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    views_counter = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return f"{self.title} - {self.created_at} - {self.views_counter}"

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = ["-created_at"]
