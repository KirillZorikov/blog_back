from math import ceil

from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'entries_count': self.page.paginator.count,
            'pages_count': ceil(
                self.page.paginator.count / settings.PAGE_SIZE
            ),
            'response': data,
        })
