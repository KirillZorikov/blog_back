# Generated by Django 2.2.6 on 2020-12-15 15:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0027_delete_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(help_text='Связь комментария c пользователями через отношение лайка.', related_name='like_comments', to=settings.AUTH_USER_MODEL, verbose_name='Лайк'),
        ),
    ]
