from django.urls import reverse

URLS = {
    'index': reverse('index'),
    'new': reverse('new'),
    'about-author': reverse('about-author'),
    'about-spec': reverse('about-spec'),
    'login': reverse('login'),
    'follow_index': reverse('follow_index'),
    'search': reverse('search') + '?search=',
}


def get_urls(include=[], group=None, user=None, post=None, tag=None):
    urls = {}
    for url_name in include:
        if url_name in ['post_edit',
                        'post',
                        'add_comment']:
            url = reverse(url_name, args=[
                user.username,
                post.pk,
            ])
        elif url_name in ['profile',
                          'profile_follow',
                          'profile_unfollow']:
            url = reverse(url_name, args=[
                user.username,
            ])
        elif url_name == 'group_posts':
            url = reverse(url_name, args=[
                group.slug,
            ])
        elif url_name == 'post_like':
            url = reverse(url_name, args=[
                post.pk,
            ])
        elif url_name == 'tag_posts':
            url = reverse(url_name, args=[
                tag.slug,
            ])
        urls[url_name] = url
    return urls if len(urls) > 1 else next(iter(urls.values()))
