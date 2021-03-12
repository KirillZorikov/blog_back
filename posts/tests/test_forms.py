import shutil
import tempfile

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.test import override_settings

from posts.models import Post, Comment
from yatube import settings
from .records import add_group, add_user, add_post
from .urls import URLS, get_urls

USERNAME = 'user'
SLUG = 'test-slug'
TEST_TEXT = 'Тестовый текст'
COMMENT_TEXT = 'текст комментария'
POST_TEXT = 'Тестовый текст'
GROUP_NAME = 'Имя сообщества'
GROUP_DESCRIPTION = 'Описание сообщества'
TAG_NAME = 'Имя тега'


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = add_user(USERNAME)
        cls.group = add_group(SLUG, GROUP_NAME, GROUP_DESCRIPTION)
        cls.urls = URLS
        cls.image = {'name': 'pic.gif',
                   'data':
                       b'\x47\x49\x46\x38\x39\x61\x02\x00'
                       b'\x01\x00\x80\x00\x00\x00\x00\x00'
                       b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                       b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                       b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                       b'\x0A\x00\x3B'
                     }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.form_fields = {
            'text': forms.fields.CharField,
            'group': forms.ModelChoiceField,
        }
        self.uploaded = SimpleUploadedFile(
            name=self.image['name'],
            content=self.image['data'],
            content_type='image/gif'
        )

    def test_create_comment(self):
        """Валидная форма создает запись в Comment.
        И передаёт в Comment ожидаемые данные."""
        self.assertEqual(Comment.objects.count(), 0)
        post = add_post(self.group, self.user, TEST_TEXT)
        form_data = {
            'text': 'COMMENT_TEXT',
        }
        url = get_urls(['add_comment'], post=post, user=self.user)
        response = self.authorized_client.post(
            url,
            data=form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), 1)
        comment = response.context.get('comments')[0]
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.text, form_data['text'])

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_post(self):
        """Валидная форма создает запись в Post.
        И передаёт в Post ожидаемые данные."""
        self.assertEqual(Post.objects.count(), 0)
        form_data = {
            'text': TEST_TEXT,
            'group': self.group.pk,
            'image': self.uploaded,
        }
        response = self.authorized_client.post(
            self.urls['new'],
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.urls['index'])
        self.assertEqual(Post.objects.count(), 1)
        post = response.context.get('page')[0]
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.pk, form_data['group'])
        self.assertEqual(post.author, self.user)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_edit_post(self):
        """После редактирования формы в Post
        попали корректные данные"""
        post = add_post(self.group, self.user, TEST_TEXT)
        urls = get_urls(['post_edit', 'post'],
                        post=post, user=self.user)
        new_group = add_group('new_slug', GROUP_NAME, GROUP_DESCRIPTION)
        self.assertEqual(Post.objects.count(), 1)
        form_data = {
            'text': post.text + 'new',
            'group': new_group.pk,
            'image': self.uploaded,
        }
        response = self.authorized_client.post(
            urls['post_edit'],
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, urls['post'])
        self.assertEqual(Post.objects.count(), 1)
        post = response.context.get('post')
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.pk, form_data['group'])

    def test_create_post_not_image_file(self):
        """Файлы не графических форматов не загружаются."""
        uploaded = SimpleUploadedFile(
            name='text.txt',
            content=b'\x47',
            content_type='text/plain'
        )
        form_data = {
            'text': TEST_TEXT,
            'group': self.group.pk,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            self.urls['new'],
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), 0)
        self.assertFormError(response, 'form', 'image',
                             ('Загрузите правильное изображение. '
                              'Файл, который вы загрузили, поврежден '
                              'или не является изображением.'))

    def test_new_page_show_correct_context(self):
        """Страница new сформирована с правильным контекстом."""
        response = self.authorized_client.get(self.urls['new'])
        for name, expected in self.form_fields.items():
            with self.subTest(name=name):
                form_field = response.context.get('form').fields.get(name)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        self.form_data = {
            'text': TEST_TEXT,
            'group': self.group.pk,
        }
        post = add_post(self.group, self.user, TEST_TEXT)
        post_edit_url = get_urls(['post_edit'], post=post,
                                 user=self.user)
        response = self.authorized_client.get(post_edit_url)
        for name, expected in self.form_data.items():
            with self.subTest(name=name):
                form_data = response.context['form'].initial[name]
                self.assertEqual(
                    str(form_data),
                    str(expected)
                )
