from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    published_at = forms.DateField(
        label='Дата публикации',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Post
        fields = ('title', 'content', 'published_at', 'views', 'is_published')

    def clean_title(self) -> str:
        title = self.cleaned_data.get('title', '')
        if not title or not title.strip():
            raise ValidationError('Заголовок не может быть пустым.')
        return title.strip()

    def clean_content(self) -> str:
        content = self.cleaned_data.get('content', '')
        if not content or not content.strip():
            raise ValidationError('Содержание не может быть пустым.')
        return content.strip()

    def clean_views(self) -> int:
        views = self.cleaned_data.get('views')
        if views is not None and views < 0:
            raise ValidationError('Количество просмотров не может быть отрицательным.')
        return views

    def clean_published_at(self):
        from django.utils import timezone

        published_at = self.cleaned_data.get('published_at')
        if published_at and published_at > timezone.localdate():
            raise ValidationError('Дата публикации не может быть в будущем.')
        return published_at

    def clean(self) -> dict:
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data

        instance = self.instance
        for field, value in cleaned_data.items():
            setattr(instance, field, value)
        try:
            instance.clean()
        except ValidationError as exc:
            if hasattr(exc, 'error_dict'):
                for field, errors in exc.error_dict.items():
                    self.add_error(field, errors)
            else:
                self.add_error(None, exc)
        return cleaned_data
