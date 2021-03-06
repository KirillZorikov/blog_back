# from django.conf.urls import handler404, handler500
# from django.contrib.flatpages import views
from django.contrib import admin
from django.urls import include, path

# handler404 = 'django_templates.posts.views.page_not_found'
# handler500 = 'django_templates.posts.views.server_error'
urlpatterns = [
    path(
        'blog/admin_panel/',
        admin.site.urls
    ),
    path('blog/api/', include('api.api_post.urls')),
    path('blog/api/', include('api.api_user.urls')),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    # path(
    #     'auth/',
    #     include('django_templates.users.urls')
    # ),
    # path(
    #     'auth/',
    #     include('django.contrib.auth.urls')
    # ),
    # path(
    #     'about/',
    #     include('django.contrib.flatpages.urls')
    # ),
    # path(
    #     'about-author/',
    #     views.flatpage,
    #     {
    #         'url': '/about-author/'
    #     },
    #     name='about-author'),
    # path(
    #     'about-spec/',
    #     views.flatpage,
    #     {
    #         'url': '/about-spec/'
    #     },
    #     name='about-spec'),
    # path(
    #     '',
    #     include('django_templates.posts.urls')
    # ),
]