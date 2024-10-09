from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from core.forms import PasswordChangeForm
from core.mixins import LoginRequiredMixins

class PasswordChangeView(LoginRequiredMixins, View):
    """
    Password change view
    """

    template_name = 'core/registration/form.html'
    form_class = PasswordChangeForm

    def get(self, request):
        """
        Get password change view
        """
        form = self.form_class(user=request.user)
        context = {
            'title': 'Password Change',
            'header': 'Password Change',
            'form_type': 'password_change',
            'form': form,
            'action': 'Password Change',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Form valid
        """
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Hi {self.request.user.username} Password has been changed successfully. Please login with your new password',
            )
            logout(request)
            return redirect(reverse('core:login'))
        return render(request, self.template_name, {'form': form})
