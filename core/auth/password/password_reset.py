from django.contrib.auth import get_user_model, views
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.forms import RequestPasswordResetForm, SetPasswordForm

class RequestPasswordResetView(views.PasswordResetView):
    """
    Password reset view
    """

    template_name = 'core/registration/form.html'
    form_class = RequestPasswordResetForm
    success_url = reverse_lazy('core:password-reset-done')
    email_template_name = 'core/auth/password/password_reset_email.html'
    subject_template_name = 'core/auth/password/password_reset_subject.txt'
    html_email_template_name = 'core/auth/password/password_reset_email.html'

    extra_context = {}

    def get_context_data(self, **kwargs):
        """
        Add the password reset form to the context data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reset Password'
        context['header'] = 'Reset Password'
        context['form_type'] = 'reset'
        context['action'] = 'Reset Password'
        context['SocialAuthentication'] = 'Reset Password with Google'
        return context

class PasswordResetDoneView(views.PasswordResetDoneView):
    """
    Password reset done view
    """

    template_name = 'core/auth/password/password_reset_done.html'

    def get_context_data(self, **kwargs):
        """
        Add the password reset form to the context data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password Reset Done'
        context['header'] = 'Password Reset Done'
        return context

class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'core/registration/form.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('core:password-reset-complete')
    html_email_template_name = (
        'core/auth/password/password_reset_confirm_email.html'
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password Reset Confirm'
        context['header'] = 'Password Reset Confirm'
        context['form_type'] = 'confirm'
        context['action'] = 'Confirm Password'
        context['SocialAuthentication'] = 'Confirm Password with Google'
        context['uidb64'] = self.kwargs['uidb64']
        context['token'] = self.kwargs['token']
        return context

    # Corrected the method signature to match the base class
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        # Get the user
        try:
            user = self.get_user(uidb64)  # Changed for clarity
        except (
            TypeError,
            ValueError,
            OverflowError,
            get_user_model().DoesNotExist,
        ):
            user = None
        if user is not None and default_token_generator.check_token(
            user, token
        ):
            # return self.form_valid(request)
            pass
        return super().get(request, *args, **kwargs)

def send_password_reset_email(request, user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    protocol = 'https' if request.is_secure() else 'http'
    domain = request.get_host()

    context = {
        'protocol': protocol,
        'domain': domain,
        'uidb64': uidb64,
        'token': token,
        'user': user,
    }

    subject = render_to_string(
        'core/auth/password/password_reset_confirm_subject.txt', context
    )
    subject = ''.join(subject.splitlines())

    email_message = render_to_string(
        'core/auth/password/password_reset_confirm_email.html', context
    )

    send_mail(
        subject,
        email_message,
        'noreply@gmail.com',
        [user.email],
        fail_silently=False,
    )

class PasswordResetCompleteView(views.PasswordResetCompleteView):
    """
    Password reset complete view
    """

    template_name = 'core/auth/password/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        """
        Add the password reset form to the context data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password Reset Complete'
        context['header'] = 'Password Reset Complete'
        return context
