import django_filters

from posts.models import Post


class PostFilter(django_filters.FilterSet):
    group = django_filters.CharFilter(field_name='group__slug', method='filter_group')
    tag = django_filters.CharFilter(field_name='tags__slug', method='filter_tag')

    class Meta:
        model = Post
        fields = ['group', 'tags']

    def filter_group(self, queryset, field_name, group):
        return queryset.filter(group__slug=group)

    def filter_tag(self, queryset, field_name, tag):
        return queryset.filter(tags__slug=tag)

