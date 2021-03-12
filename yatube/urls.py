from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"
urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path(
        'auth/',
        include('users.urls')
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
    path(
        'blog_admin/',
        admin.site.urls
    ),
    path(
        'about/',
        include('django.contrib.flatpages.urls')
    ),
    path(
        'about-author/',
        views.flatpage,
        {
            'url': '/about-author/'
        },
        name='about-author'),
    path(
        'about-spec/',
        views.flatpage,
        {
            'url': '/about-spec/'
        },
        name='about-spec'),
    path(
        '',
        include('posts.urls')
    ),
    path('api/', include('api.api_post.urls')),
    path('api/', include('api.api_user.urls')),
]
