from django.contrib.flatpages.models import FlatPage
from django.test import Client, TestCase

from posts.models import User
from .records import add_group, add_tag, add_user, add_post
from .urls import URLS, get_urls

USERNAME = 'user'
SLUG = 'test-slug'
TEST_TEXT = 'Тестовый текст'
GROUP_NAME = 'Имя сообщества'
GROUP_DESCRIPTION = 'Описание сообщества'
TAG_NAME = 'Имя тега'






class UrlsAccess(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = add_user(USERNAME)
        cls.group = add_group(SLUG, GROUP_NAME, GROUP_DESCRIPTION)
        cls.post = add_post(cls.group, cls.user, TEST_TEXT)
        cls.tag = add_tag(SLUG, TAG_NAME)
        include = ['profile', 'post',
                   'post_edit', 'group_posts',
                   'profile_follow', 'add_comment',
                   'post_like', 'tag_posts',
                   'profile_unfollow']
        calc_urls = get_urls(include, cls.group, cls.user,
                             cls.post, cls.tag)
        cls.urls = {**URLS, **calc_urls}

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_locations(self):
        """Проверка доступности адресов."""
        guest_access_urls = [
            '/',
            self.urls['profile'],
            self.urls['group_posts'],
            self.urls['post'],
            self.urls['index'],
            self.urls['search'],
            self.urls['tag_posts']
        ]
        auth_access_urls = [
            self.urls['new'],
            self.urls['post_edit'],
            self.urls['add_comment'],
            self.urls['profile_follow'],
            self.urls['post_like'],
        ]

        for url in guest_access_urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
        for url in auth_access_urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)

    def test_redirect_anonymous_on_login(self):
        """Проверка перенаправления анонимного пользователя
        на страницу логина."""
        urls = [
            self.urls['new'],
            self.urls['post_edit'],
            self.urls['follow_index'],
            self.urls['add_comment'],
            self.urls['profile_follow'],
            self.urls['profile_unfollow'],
            self.urls['post_like'],
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(
                    response,
                    f"{self.urls['login']}?next={url}"
                )

    def test_post_edit_url_not_author_access(self):
        """Страница по адресу /<username>/<post_id>/edit/ перенаправит
        пользователя на страницу /<username>/<post_id>/,
        если тот не автор записи, которую желает редактировать."""
        user = User.objects.create_user(
            username='user2'
        )
        self.authorized_client.force_login(user)
        response = self.authorized_client.get(self.urls['post_edit'])
        self.assertRedirects(response, self.urls['post'])

    def test_page_not_found(self):
        """Несуществующая страница вернёт код 404."""
        url = '/nonexist/'
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 404)


class FlatPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        author = FlatPage.objects.create(
            url=URLS['about-author'],
            content='Текст'
        )
        spec = FlatPage.objects.create(
            url=URLS['about-spec'],
            content='Текст'
        )
        author.sites.add(1)
        spec.sites.add(1)

    def test_flatpages_location(self):
        """Проверка доступности flatpages адресов."""
        response = self.guest_client.get(URLS['about-author'])
        self.assertEqual(response.status_code, 200)
        response = self.guest_client.get(URLS['about-spec'])
        self.assertEqual(response.status_code, 200)

    def test_flatpages_uses_correct_template(self):
        """flatpages используют шаблон flatpages/default.html."""
        response = self.guest_client.get(URLS['about-author'])
        self.assertTemplateUsed(response, 'flatpages/default.html')
        response = self.guest_client.get(URLS['about-spec'])
        self.assertTemplateUsed(response, 'flatpages/default.html')
