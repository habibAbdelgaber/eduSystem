from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import edit

from core.forms import SignupForm
from core.tokens import email_verification_token

User = get_user_model()

class SignupView(edit.CreateView, SuccessMessageMixin):
    """
    Signup View
    """

    template_name = 'core/registration/form.html'
    form_class = SignupForm
    success_url = reverse_lazy('index')
    success_message = 'You have just registered 💪! Please check your email to confirm your account'
    # permanent = False  # Use temporary redirect (302)

    # def get_success_url(self):
    #     return super().get_success_url()

    def get_context_data(self, **kwargs):
        """
        Add the signup form to the context data
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign up'
        context['header'] = 'Sign up'
        context['form_type'] = 'signup'
        context['action'] = 'Sign up'
        context['socialAuthentication'] = 'Sign up with Google'
        return context

    def form_valid(self, form):
        """
        Handle successful signup
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_email_confirmation(self.request, user)
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle unsuccessful signup
        """
        return super().form_invalid(form)

def send_email_confirmation(request, user):
    """
    Send activation email
    """
    token = email_verification_token.make_token(user)
    # token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    # domain = get_current_site(request).domain
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
        'core/auth/email/email_verification_subject.txt'
    )
    subject = ''.join(subject.splitlines())
    html = render_to_string('core/auth/email/email_verification.html', context)
    plain = render_to_string('core/auth/email/email_verification.txt', context)

    send_mail(
        subject,
        plain,
        # settings.DEFAULT_FROM_EMAIL,
        'noreply@gmail.com',
        [user.email],
        html_message=html,
    )
