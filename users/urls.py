from django.contrib.auth.views import LoginView
from django.urls import path

from . import views
from .decorators import check_recaptcha

urlpatterns = [
    path('signup/',
         check_recaptcha(views.SignUp.as_view()),
         name='signup'),
    path('login/',
         LoginView.as_view(template_name='registration/login.html',
                           redirect_authenticated_user=True),
         name='login'),
]
