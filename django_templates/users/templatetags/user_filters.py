from django import template

register = template.Library()


@register.filter
def add_attr(field, attrs):
    dic = {}
    for attr in attrs.split(','):
        arg, val = attr.split('=')
        dic[arg] = val
    return field.as_widget(attrs=dic)


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def get_page_param(number):
    return f'page={number}&' if number and number > 1 else ''
