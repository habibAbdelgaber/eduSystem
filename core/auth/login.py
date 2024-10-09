# from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from core.forms import LoginForm

class LoginView(views.LoginView, SuccessMessageMixin):
    """
    Custom Login View
    """

    template_name = 'core/registration/form.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:index')
    success_message = 'You have signed in'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(
            self.request,
            f'Hi {self.request.user.username}.  {self.success_message}',
        )
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        """
        Add the login form to the context data
        """
        # print(self.request.build_absolute_uri())
        # print(self.request.get_host())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log in'
        context['header'] = 'Log in'
        context['form_type'] = 'login'
        context['action'] = 'Log in'
        context['socialAuthentication'] = 'Log in with Google'
        return context

    def form_valid(self, form):
        """
        Handle successful login
        """
        remember_me = self.request.POST.get('remember_me', None)
        user = authenticate(
            self.request,
            email=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None and user.is_active:
            login(self.request, user)

        if remember_me:
            """
            Session expiried within 2 weeks
            """
            # print(self.request.session.session_key)
            self.request.session.set_expiry(60 * 60 * 24 * 14)
        else:
            self.request.session.set_expiry(
                0
            )  # Session will be expired immediately when the Browser close
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle unsuccessful login
        """
        return super().form_invalid(form)
