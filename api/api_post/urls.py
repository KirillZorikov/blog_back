from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    'posts',
    views.PostViewSet,
    basename='posts',
)
router.register(
    'group',
    views.GroupViewSet,
    basename='group',
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