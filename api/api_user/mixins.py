import requests
from django.conf import settings
from requests import RequestException
from rest_framework import serializers


class RecaptchaValidationMixin:
    def validate_recaptcha_key(self, value):
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': value
        }
        try:
            response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data=data
            ).json()
        except RequestException:
            raise serializers.ValidationError(
                {'recaptcha': 'Recaptcha is not available now. Try again.'}
            )
        if 'success' not in response:
            raise serializers.ValidationError(
                {'recaptcha': ('Something went wrong. If the error continues to appear, '
                               'write to the administrator.')}
            )
        if not response['success']:
            raise serializers.ValidationError(
                {'recaptcha': 'Enter recaptcha!'}
            )
        return value
