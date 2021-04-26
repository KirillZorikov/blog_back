import os

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Exists, OuterRef, Sum
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

User = get_user_model()


class ModelQuerySet(models.QuerySet):
    def annotate_like_dislike(self, user):
        return self.annotate(
            liked=Exists(
                LikeDislike.objects.filter(
                    user=user.id,
                    # content_type=ContentType.objects.get_for_model(self.model),
                    content_type__model=self.model.__name__.lower(),
                    object_id=OuterRef('id'),
                    vote=LikeDislike.LIKE
                ).only('id')
            )
        ).annotate(
            disliked=Exists(
                LikeDislike.objects.filter(
                    user=user.id,
                    content_type__model=self.model.__name__.lower(),
                    object_id=OuterRef('id'),
                    vote=LikeDislike.DISLIKE
                ).only('id')
            )
        )


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def rating(self):
        return self.get_queryset().aggregate(
            Sum('vote')
        ).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name='Голос', choices=VOTES)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    class Meta:
        unique_together = ('user', 'object_id')


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


class Post(models.Model):
    text = RichTextField(
        verbose_name='Текст',
        help_text='Введите текст новой записи.'
    )
    text_preview = models.TextField(
        verbose_name='Превью',
        help_text='Превью текста поста.'
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
    votes = GenericRelation(LikeDislike, related_query_name='posts')

    objects = ModelQuerySet.as_manager()

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    @property
    def image_name(self):
        return os.path.basename(self.image.path) if self.image else ''

    def __str__(self):
        return self.text[:15]

    def save(self, *args, **kwargs):
        if len(self.text) > 200:
            self.text_preview = self.text[:200] + '...'
        else:
            self.text_preview = self.text[:len(self.text) // 2] + '...'
        super().save(*args, **kwargs)


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
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    objects = ModelQuerySet.as_manager()

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
