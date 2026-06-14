from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post


class PingIntegrationTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_ping_returns_200(self) -> None:
        response = self.client.get('/ping/')
        self.assertEqual(response.status_code, 200)

    def test_index_returns_200(self) -> None:
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class PostFormValidationTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.post = Post.objects.create(title='Тест', content='Содержание')

    def test_create_invalid_shows_form_with_errors(self) -> None:
        response = self.client.post(
            reverse('create'),
            {
                'title': '',
                'content': '',
                'published_at': '2099-01-01',
                'views': '-1',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Не удалось сохранить пост')
        self.assertContains(response, 'Заголовок не может быть пустым')
        self.assertEqual(Post.objects.count(), 1)

    def test_update_invalid_shows_form_with_errors(self) -> None:
        response = self.client.post(
            reverse('update', args=[self.post.pk]),
            {
                'title': '   ',
                'content': 'Содержание',
                'published_at': '2099-01-01',
                'views': '0',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Не удалось сохранить пост')
        self.assertContains(response, 'Дата публикации не может быть в будущем')
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Тест')
