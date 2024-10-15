"""
Core users account deletion
"""

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from core.mixins import LoginRequiredMixins

User = get_user_model()

class AccountDeletionView(
    LoginRequiredMixins, UserPassesTestMixin, DeleteView, SuccessMessageMixin
):
    """
    Account deletion view
    """

    model = User
    success_url = reverse_lazy('core:login')
    success_message = 'Your account has been deleted permanently!'

    def test_func(self):
        """
        Check if the user is authenticated
        """
        user = self.get_object()
        return self.request.user == user and not self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        """
        Delete the user and log the user out after deletion
        """
        # user = self.get_object()
        response = super().delete(request, *args, **kwargs)
        logout(request)
        print(response)
        return response

    def get(self, request, *args, **kwargs):
        """
        Performing the deletion directly via GET without a POST request or confirmation template
        """
        return self.post(request, *args, **kwargs)
