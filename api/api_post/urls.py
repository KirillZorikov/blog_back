from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(
    'posts',
    views.PostViewSet,
    basename='posts',
)
router.register(
    'groups',
    views.GroupViewSet,
    basename='group',
)
router.register(
    'tags',
    views.TagViewSet,
    basename='tag',
)
router.register(
    'follow',
    views.FollowViewSet,
    basename='follow',
)
router.register(
    r'posts/(?P<post_id>[^/.]+)/comments',
    views.CommentViewSet,
    basename='comments',
)
urlpatterns = [
    path('v1/', include(router.urls)),
]