from django.contrib.auth import authenticate
from rest_framework import serializers


def authenticate_user(password, username=None, email=None):
    user = authenticate(username=username or email, password=password)
    if user is None:
        raise serializers.ValidationError('Invalid data. '
                                          'Please try again!')
    return user
