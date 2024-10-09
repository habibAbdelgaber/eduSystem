from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import UserPassesTestMixin
from core.mixins import LoginRequiredMixins
from core.forms import UserChangeForm, UserProfileForm


class UserUpdateView(LoginRequiredMixins, UpdateView, SuccessMessageMixin):
    """
    User update view
    """
    model = get_user_model()
    template_name = 'users/details.html'
    form_class = UserChangeForm
    profile_form_class = UserProfileForm
    success_url = reverse_lazy('index')
    success_message = 'Your profile has been updated.'
    

    def get_object(self, queryset=None):
        """
        Get the object to be updated
        """
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        """
        Get the context data
        """
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            profile = self.request.user.profile
            context['profile_form'] = self.profile_form_class(self.request.POST or None, self.request.FILES or None, instance=profile)
        context['title'] = 'User Profile'
        context['action'] = 'Update Profile'
        return context

    def form_valid(self, form):
        """
        Form valid
        """
        context = self.get_context_data()
        profile_form = context['profile_form']
        if profile_form.is_valid():
            profile_form.save()
            messages.success(self.request, self.success_message)

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Form invalid
        """
        context = self.get_context_data()
        if 'profile_form' not in context:
            messages.error(self.request, 'Unable to update profile')
        return super().form_invalid(form)
    def test_func(self):
        """
        Check if the user is authenticated
        """
        return self.request.user.user_id == self.kwargs.get('pk')
        

    