# Generated by Django 2.2.6 on 2021-02-15 09:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0030_auto_20201218_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='dislikes',
            field=models.ManyToManyField(blank=True, help_text=('Связь комментария c пользователями ', 'через отношение дизлайка.'), related_name='dislike_comments', to=settings.AUTH_USER_MODEL, verbose_name='ДизЛайк'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, help_text=('Связь комментария c пользователями', ' через отношение лайка.'), related_name='like_comments', to=settings.AUTH_USER_MODEL, verbose_name='Лайк'),
        ),
        migrations.AlterField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(blank=True, help_text=('Связь поста c пользователями ', 'через отношение дизлайка.'), related_name='dislikes_post', to=settings.AUTH_USER_MODEL, verbose_name='ДизЛайк'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, help_text=('Связь поста c пользователями ', 'через отношение лайка.'), related_name='likes_post', to=settings.AUTH_USER_MODEL, verbose_name='Лайк'),
        ),
    ]
