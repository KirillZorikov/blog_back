from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'signup.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # проверка валидности reCAPTCHA
        if self.request.recaptcha_is_valid:
            user = form.save()
            login(
                self.request,
                user,
                backend='django.contrib.auth.backends.ModelBackend'
            )
            messages.success(
                self.request,
                'Вы успешно зарегистрировались!'
            )
            return redirect('index')
        return render(self.request, 'signup.html', self.get_context_data())