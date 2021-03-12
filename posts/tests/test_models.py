from django.test import TestCase

from .records import add_group, add_tag, add_user
from .records import add_post, add_follow, add_comment

USERNAME = 'user'
SLUG = 'test-slug'
TEST_TEXT = 'Тестовый текст'
COMMENT_TEXT = 'текст комментария'
GROUP_NAME = 'Имя сообщества'
GROUP_DESCRIPTION = 'Описание сообщества'
TAG_NAME = 'Имя тега'


class ModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = add_user(USERNAME)
        cls.group = add_group(SLUG, GROUP_NAME, GROUP_DESCRIPTION)
        cls.post = add_post(cls.group, cls.user, TEST_TEXT)
        cls.tag = add_tag(SLUG, TAG_NAME)
        cls.comment = add_comment(cls.post, cls.user, COMMENT_TEXT)
        author = add_user('author')
        cls.follow = add_follow(author, cls.user)

    def test_group_model_verbose_help_str(self):
        """Проверка verbose_name, help_text и str у Group."""
        field_verboses = {
            'title': 'Имя сообщества',
            'slug': 'Ключ для построения ссылки',
            'description': 'Описание',
        }
        field_help_texts = {
            'title': 'Дайте сообществу имя.',
            'slug': 'Укажите адрес для страницы сообщества.',
            'description': 'Опишите деятельность сообщества.',
        }
        self.assertEqual(self.group.title, str(self.group))
        for name, expected in field_verboses.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.group._meta.get_field(name).verbose_name,
                    expected
                )
        for name, expected in field_help_texts.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.group._meta.get_field(name).help_text,
                    expected
                )

    def test_post_model_verbose_help_str(self):
        """Проверка verbose_name, help_text и str у Proup."""
        field_verboses = {
            'group': 'Сообщество',
            'author': 'Автор',
            'text': 'Текст',
            'pub_date': 'Дата',
        }
        field_help_texts = {
            'group': 'Сообщество, с которым связана запись.',
            'author': 'Автор записи.',
            'text': 'Введите текст новой записи.',
            'pub_date': 'Дата публикации записи.',
        }
        self.assertEqual(self.post.text[:15], str(self.post))
        for name, expected in field_verboses.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.post._meta.get_field(name).verbose_name,
                    expected
                )
        for name, expected in field_help_texts.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.post._meta.get_field(name).help_text,
                    expected
                )

    def test_comment_model_verbose_help_str(self):
        """Проверка verbose_name, help_text и str у Comment."""
        field_verboses = {
            'post': 'Запись',
            'text': 'Текст',
            'author': 'Автор',
            'created': 'Дата',
        }
        field_help_texts = {
            'post': 'Комментируемая запись.',
            'text': 'Текст комментария.',
            'author': 'Автор комментария.',
            'created': 'Дата отправки комментария.',
        }
        self.assertEqual(self.comment.text[:15], str(self.comment))
        for name, expected in field_verboses.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.comment._meta.get_field(name).verbose_name,
                    expected
                )
        for name, expected in field_help_texts.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.comment._meta.get_field(name).help_text,
                    expected
                )

    def test_follow_model_verbose_help_str(self):
        """Проверка verbose_name и help_text у Follow."""
        field_verboses = {
            'author': 'Подписываемый',
            'user': 'Подписывающийся',
        }
        field_help_texts = {
            'author': 'Пользователь, на которого подписываются.',
            'user': 'Пользователь, который подписывается.',
        }
        for name, expected in field_verboses.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.follow._meta.get_field(name).verbose_name,
                    expected
                )
        for name, expected in field_help_texts.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.follow._meta.get_field(name).help_text,
                    expected
                )

    def test_tag_model_verbose_help_str(self):
        """Проверка verbose_name, help_text и str у Tag."""
        field_verboses = {
            'title': 'Имя тега',
            'slug': 'Ключ для построения ссылки',
        }
        field_help_texts = {
            'title': 'Введите имя тега.',
            'slug': 'Укажите адрес для страницы тега.',
        }
        self.assertEqual(self.tag.title, str(self.tag))
        for name, expected in field_verboses.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.tag._meta.get_field(name).verbose_name,
                    expected
                )
        for name, expected in field_help_texts.items():
            with self.subTest(name=name):
                self.assertEqual(
                    self.tag._meta.get_field(name).help_text,
                    expected
                )
