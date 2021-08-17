from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    """Статья"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Автор',
        on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название поста', max_length=255)
    text = models.TextField()
    # Аналог ForeignKey, comment - название модели
    comments = GenericRelation('comment')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    """Комметарий"""

    # AUTH_USER_MODEL - дефолтная модель пользователя в Django
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Автор',
        on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    parent = models.ForeignKey(
        'self', verbose_name='Родительский комментарий', null=True, blank=True,
        related_name='comment_children', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(
        verbose_name='Дата создания', auto_now=True)

    content_type = models.ForeignKey(
        ContentType, verbose_name='Все модели (ContentType)',
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(
        verbose_name='ID Статьи (object_id)')
    is_child = models.BooleanField(
        verbose_name='Дочерний комментарий', default=False)

    @property
    def get_parent(self):
        """При отсутствии родителя вернуть пустую строку"""
        if not self.parent:
            return ""
        return self.parent

    def __str__(self):
        return f'Комментарий № {str(self.id)} от {self.user}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
