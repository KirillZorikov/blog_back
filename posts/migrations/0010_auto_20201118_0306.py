# Generated by Django 2.2.6 on 2020-11-17 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20201118_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(help_text='Укажите адрес для страницы сообщества.', unique=True, verbose_name='Ключ для построения ссылки'),
        ),
    ]
