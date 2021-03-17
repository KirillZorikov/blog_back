from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField('Email',
                              max_length=100,
                              unique=True,
                              help_text='Email пользователя.',
                              )


User = get_user_model()
