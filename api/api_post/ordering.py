from django.db.models import Count
from rest_framework.filters import OrderingFilter


class PostCustomOrdering(OrderingFilter):
    allowed_custom_filters = ['rating', 'comments_count', 'pub_date',
                              '-rating', '-comments_count', '-pub_date']

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)

        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = [f for f in fields if f in self.allowed_custom_filters]
            if ordering:
                return ordering

        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):

        ordering = self.get_ordering(request, queryset, view)
        print(ordering)
        if not ordering:
            return queryset
        for order in ordering:
            if 'comments_count' in order:
                queryset = queryset.annotate(comments_count=Count('comments'))
        return queryset.order_by(*ordering)
