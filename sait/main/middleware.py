from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import UserActionLog


class LoginRequiredMiddleware:
    EXEMPT_URLS = [
        '/admin/',
        reverse('login'),
        '/static/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Проверяем аутентификацию и истечение сессии
        if not any(path.startswith(url) for url in self.EXEMPT_URLS):
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)
            # Проверка, не истекла ли сессия
            if request.session.get_expiry_age() <= 0:
                from django.contrib.auth import logout
                logout(request)
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)

class UserActionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            UserActionLog.objects.create(
                user=request.user,
                action=f"Посетил страницу {request.method}",
                path=request.path
            )
        return response