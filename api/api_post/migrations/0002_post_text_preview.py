# Generated by Django 2.2.6 on 2021-03-17 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text_preview',
            field=models.TextField(default=None, help_text='Превью текста поста.', verbose_name='Превью'),
            preserve_default=False,
        ),
    ]
