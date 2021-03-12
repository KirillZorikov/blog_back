import os

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.db.models import Exists, OuterRef

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def annotate_like(self, user):
        return self.annotate(
            liked=Exists(
                Like.objects.filter(user=user.id, post_id=OuterRef('id')).only('id')
            )
        )


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Имя сообщества',
        help_text='Дайте сообществу имя.'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Ключ для построения ссылки',
        help_text='Укажите адрес для страницы сообщества.'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Опишите деятельность сообщества.'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        get_latest_by = 'id'
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='likes', on_delete=models.CASCADE)

    class Meta:
        ordering = ('user',)
        unique_together = ('user', 'post')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.user} liked {self.post}'


class Post(models.Model):
    text = RichTextField(
        verbose_name='Текст',
        help_text='Введите текст новой записи.'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
        help_text='Дата публикации записи.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор записи.'
    )
    group = models.ForeignKey(
        Group,
        related_name='posts',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Сообщество',
        help_text='Сообщество, с которым связана запись.'
    )
    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Картинка',
        help_text='Кртинка к записи.',
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='posts',
        blank=True,
        verbose_name='Теги',
        help_text='Теги, подходящие к записи.'
    )

    objects = PostQuerySet.as_manager()

    @property
    def image_name(self):
        return os.path.basename(self.image.path) if self.image else ''

    def __str__(self):
        return self.text[:15]

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(MPTTModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Запись',
        help_text='Комментируемая запись.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария.'
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст комментария.'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
        help_text='Дата отправки комментария.'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # likes = models.ManyToManyField(
    #     User,
    #     related_name='like_comments',
    #     verbose_name='Лайк',
    #     blank=True,
    #     help_text=('Связь комментария c пользователями',
    #                ' через отношение лайка.')
    # )
    # dislikes = models.ManyToManyField(
    #     User,
    #     related_name='dislike_comments',
    #     verbose_name='ДизЛайк',
    #     blank=True,
    #     help_text=('Связь комментария c пользователями ',
    #                'через отношение дизлайка.')
    # )
    #
    # def add_like(self, user):
    #     like_exists = self.likes.filter(id=user.id).exists()
    #     dislike_exists = self.dislikes.filter(id=user.id).exists()
    #     if like_exists:
    #         self.likes.remove(user)
    #     else:
    #         self.likes.add(user)
    #     if dislike_exists:
    #         self.dislikes.remove(user)
    #
    # def add_dislike(self, user):
    #     like_exists = self.likes.filter(id=user.id).exists()
    #     dislike_exists = self.dislikes.filter(id=user.id).exists()
    #     if dislike_exists:
    #         self.dislikes.remove(user)
    #     else:
    #         self.dislikes.add(user)
    #     if like_exists:
    #         self.likes.remove(user)

    def __str__(self):
        return self.text[:15]

    class MPTTMeta:
        order_insertion_by = ['created']
        get_latest_by = 'created'
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Пользователь, который подписывается.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Пользователь, на которого подписываются.'
    )

    class Meta:
        ordering = ('user',)
        unique_together = ('user', 'author')
        verbose_name = 'Подписка(у)'
        verbose_name_plural = 'Подписки'


class Tag(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Имя тега',
        help_text='Введите имя тега.'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Ключ для построения ссылки',
        help_text='Укажите адрес для страницы тега.'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        get_latest_by = 'id'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
