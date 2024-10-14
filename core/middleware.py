"""
Core middleware
"""
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import Resolver404, resolve, reverse

class RedirectAuthenticatedUserMiddleware:
    """
    Redirect authenticated user to the home page
    """

    def __init__(self, get_response):
        """
        Initialize the middleware
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Redirect authenticated user to the home page
        """
        if request.user.is_authenticated and request.path in [
            reverse('core:login'),
            reverse('core:signup'),
        ]:
            request.path = ''
            messages.info(request, 'You are already logged in')
            return redirect(reverse('index'))
        return self.get_response(request)

class UrlNotFoundInterceptionMiddleware:
    """
    Intercept 404 errors and redirect to the home page
    """

    def __init__(self, get_response):
        """
        Initialize the middleware
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Intercept 404 errors and redirect to the home page
        """
        allowed_paths = ['/django-admin/']
        if request.path_info in allowed_paths:
            return self.get_response(request)
        try:
            resolve(request.path_info)

        except Resolver404:
            return redirect(reverse('index'))

        return self.get_response(request)
