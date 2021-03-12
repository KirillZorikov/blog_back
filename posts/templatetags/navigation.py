from django import template
from django.db.models import Count

from posts.models import Group, Tag

register = template.Library()


@register.inclusion_tag('nav_groups.html')
def get_groups(cnt=10, slug=None):
    groups = Group.objects.annotate(
        count=Count('posts')
    ).order_by('-count')[:cnt]
    return {'groups': groups, 'slug': slug}


@register.inclusion_tag('nav_tags.html')
def get_tags():
    tags = Tag.objects.all()
    return {'tags': tags}


