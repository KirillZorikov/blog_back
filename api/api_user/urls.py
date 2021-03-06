from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import AuthViewSet, UserInfo

router = routers.DefaultRouter(trailing_slash=False)
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserInfo, basename='user_info')

urlpatterns = [
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router.urls)),
]
