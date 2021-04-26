import tempfile

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.test import override_settings

from posts.models import Post, Follow
from yatube import settings
from .records import add_group, add_tag, add_user
from .records import add_post, add_follow
from .urls import URLS, get_urls


USERNAME = 'user'
SLUG = 'test-slug'
TEST_TEXT = 'Тестовый текст'
GROUP_NAME = 'Имя сообщества'
GROUP_DESCRIPTION = 'Описание сообщества'
TAG_NAME = 'Имя тега'


class TemplatePageTest(TestCase):
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
                   'post_like', 'tag_posts']
        calc_urls = get_urls(include, cls.group, cls.user,
                             cls.post, cls.tag)
        cls.urls = {**URLS, **calc_urls}

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates = {
            self.urls['index']: 'posts/index.html',
            self.urls['group_posts']: 'posts/group.html',
            self.urls['new']: 'posts/add_post.html',
            self.urls['profile']: 'posts/profile.html',
            self.urls['post']: 'posts/post.html',
            self.urls['post_edit']: 'posts/add_post.html',
            self.urls['follow_index']: 'posts/follow.html',
            self.urls['add_comment']: 'posts/post.html',
            self.urls['profile_follow']: 'posts/profile.html',
            self.urls['search']: 'search.html',
            self.urls['post_like']: 'posts/index.html',
            self.urls['post_like'] + f'?next={self.urls["post"]}':
                'posts/post.html',
            self.urls['tag_posts']: 'posts/tag.html',
        }
        for reverse_name, template in templates.items():
            with self.subTest(url=reverse_name):
                response = self.authorized_client.get(reverse_name,
                                                      follow=True)
                self.assertTemplateUsed(response, template)


class ContextTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.user = add_user(USERNAME)
        cls.group = add_group(SLUG, GROUP_NAME, GROUP_DESCRIPTION)
        cls.tag = add_tag(SLUG, TAG_NAME)
        cls.post = add_post(cls.group, cls.user, TEST_TEXT, cls.tag)
        include = ['profile', 'post',
                   'post_edit', 'group_posts',
                   'profile_follow', 'add_comment',
                   'post_like', 'tag_posts',
                   'profile_unfollow']
        calc_urls = get_urls(include, cls.group, cls.user,
                             cls.post, cls.tag)
        cls.urls = {**URLS, **calc_urls}
        cls.image = {'name': 'pic.gif',
                   'data':
                       b'\x47\x49\x46\x38\x39\x61\x02\x00'
                       b'\x01\x00\x80\x00\x00\x00\x00\x00'
                       b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                       b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                       b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                       b'\x0A\x00\x3B'
                     }

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_author = self.user
        self.follower_user = add_user('user1')
        self.not_follower_user = add_user('user2')
        cache.clear()

    def test_pages_show_correct_context(self):
        """Шаблоны сформированы с правильным контекстом."""
        urls = {
            self.urls['index']: ['groups', 'page'],
            self.urls['profile']: ['page'],
            self.urls['group_posts']: ['page'],
            self.urls['post']: ['post'],
            self.urls['tag_posts']: ['page'],
        }
        for url, names in urls.items():
            response = self.authorized_client.get(url)
            for name in names:
                with self.subTest(url=url):
                    if name == 'post':
                        val_context = response.context.get(name)
                    else:
                        val_context = response.context.get(name)[0]
                    if name == 'groups':
                        self.assertEqual(
                            self.group,
                            val_context
                        )
                    else:
                        self.assertEqual(
                            self.post,
                            val_context
                        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_image_show(self):
        """Пост с картинкой корректно отображается."""
        uploaded = SimpleUploadedFile(
            name=self.image['name'],
            content=self.image['data'],
            content_type='image/gif'
        )
        add_post(self.group, self.user, TEST_TEXT, img=uploaded)
        response = self.authorized_client.get(self.urls['index'])
        self.assertContains(response, 'img')

    def test_cache_index(self):
        """Главная страница кэшируется."""
        response = self.authorized_client.get(self.urls['index'])
        content = response.content
        add_post(self.group, self.user, TEST_TEXT)
        response = self.authorized_client.get(self.urls['index'])
        self.assertEqual(response.content, content)
        cache.clear()
        response = self.authorized_client.get(self.urls['index'])
        self.assertNotEqual(response.content, content)

    def test_search_show_found_posts(self):
        """Страница поиска вернёт найденные записи."""
        response = self.authorized_client.get(
            self.urls['search'] + self.post.text
        )
        self.assertEqual(len(response.context.get('page')), 1)

    def test_search_not_found_any(self):
        """Страница поиска не вернёт никаких записей,
         если те не были найдены"""
        response = self.authorized_client.get(
            self.urls['search'] + self.post.text * 2
        )
        self.assertEqual(len(response.context.get('page')), 0)

    def test_post_for_follower(self):
        """Новая запись пользователя появляется в ленте тех, кто на него
        подписан."""
        self.authorized_client.force_login(self.follower_user)
        add_follow(self.post_author, self.follower_user)
        response = self.authorized_client.get(self.urls['follow_index'])
        self.assertEqual(len(response.context.get('page')), 1)
        post = response.context.get('page')[0]
        self.assertEqual(post, self.post)

    def test_post_for_not_follower(self):
        """Новая запись пользователя не появляется в ленте тех, кто на него
        не подписан."""
        add_follow(self.post_author, self.follower_user)
        self.assertEqual(Follow.objects.all().count(), 1)
        self.authorized_client.force_login(self.not_follower_user)
        response = self.authorized_client.get(self.urls['follow_index'])
        self.assertEqual(len(response.context.get('page')), 0)

    def test_follow(self):
        """Авторизованный пользователь может подписываться на
        других пользователей."""
        self.authorized_client.force_login(self.follower_user)
        self.assertEqual(Follow.objects.count(), 0)
        self.authorized_client.get(self.urls['profile_follow'])
        self.assertEqual(Follow.objects.count(), 1)
        follow = Follow.objects.last()
        self.assertEqual(follow.author, self.post_author)
        self.assertEqual(follow.user, self.follower_user)

    def test_unfollow(self):
        """Авторизованный пользователь может удалять пользователей из
         своих подписок."""
        add_follow(self.post_author, self.follower_user)
        self.authorized_client.force_login(self.follower_user)
        self.assertEqual(Follow.objects.all().count(), 1)
        self.authorized_client.get(self.urls['profile_unfollow'])
        self.assertEqual(Follow.objects.count(), 0)

    def test_paginator_with_correct_context(self):
        """paginator передает в контекст не более
        установленного число записей."""
        for i in range(15):
            Post.objects.create(
                author=self.user,
                text='Тестовый текст поста ' + str(i)
            )
        response = self.authorized_client.get(self.urls['index'])
        posts_count_exp = 10
        self.assertEqual(len(response.context['page'].object_list),
                         posts_count_exp)
