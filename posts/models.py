from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    published_at = models.DateField('Дата публикации', default=timezone.localdate)
    views = models.IntegerField('Просмотры', default=0)
    is_published = models.BooleanField('Опубликован', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        super().clean()
        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Заголовок не может быть пустым.'})
        if not self.content or not self.content.strip():
            raise ValidationError({'content': 'Содержание не может быть пустым.'})
        if self.published_at and self.published_at > timezone.localdate():
            raise ValidationError(
                {'published_at': 'Дата публикации не может быть в будущем.'}
            )
        if self.views is not None and self.views < 0:
            raise ValidationError({'views': 'Количество просмотров не может быть отрицательным.'})
