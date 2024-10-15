"""
Core muxins
"""

from django.contrib import messages
from django.contrib.auth import mixins
from django.urls import reverse_lazy

class LoginRequiredMixins(mixins.LoginRequiredMixin):
    """
    Login required mixin
    """

    login_url = reverse_lazy('core:login')

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the user is authenticated
        """
        if not request.user.is_authenticated:
            messages.error(
                request, 'You must be logged in to access this page'
            )
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
