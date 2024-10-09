import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from core.forms import EmailVerificationResendForm
from core.tokens import email_verification_token

logger = logging.getLogger(__name__)

class EmailVerificationView(View):
    """
    Email verification view
    """

    def get_success_url(self):
        """
        Redirect to login page
        """
        return reverse_lazy('core:login')

    def get(self, request, uidb64, token):
        try:
            uidb64 = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uidb64)
            logger.debug(f"Decoded UID {uidb64} to user {user}")
        except (
            TypeError,
            ValueError,
            OverflowError,
            get_user_model().DoesNotExist,
        ) as e:
            user = None
            logger.error(f"Error decoding UID or fetching user: {e}")

        if user is not None:
            logger.debug("User found, checking token")
            if email_verification_token.check_token(user, token):
                logger.debug("Token is valid")
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.success(
                        request,
                        'Your account has been verified, you can go ahead and login now.',
                    )
                    return redirect(self.get_success_url())
                else:
                    messages.info(
                        request,
                        'Your account is already verified. Please login.',
                    )
                    return redirect(self.get_success_url())
            else:
                logger.warning("Token is invalid")

        messages.error(
            request,
            'Email verification failed. Please request a new verification link. and try again.',
        )
        return render(request, 'core/auth/email/verification_invalid.html')

class RequestEmailVerificationView(View, SuccessMessageMixin):
    """
    Request email verification view
    """

    form_class = EmailVerificationResendForm
    template_name = 'core/registration/form.html'
    # success_url = reverse_lazy('core:login')
    success_message = 'An email has been sent to your email address. Please check your email to verify your accouny'

    def get_success_url(self):
        """
        Redirect to login page
        """
        return reverse_lazy('core:login')

    def get_url(self):
        """
        Get the URL to redirect
        """
        return reverse_lazy('core:email-verification')

    def get(self, request):
        """
        Render the request email verification page
        """
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in')
            return redirect(reverse('index'))
        form = self.form_class(request.GET or None)
        context = {
            'title': 'Request email verification',
            'header': 'Request email verification',
            'form': form,
            'form_type': 'request_verification',
            'action': 'Request email verification',
            'SocialAuthentication': 'Request email verification with Google',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Request email verification
        """
        email = request.POST.get('email')
        form = self.form_class(request.POST)
        if form.is_valid():
            user = get_user_model().objects.filter(email=email).first()
            if user is not None:
                send_email_verification(request, user)
                messages.success(request, self.success_message)
                return redirect(self.get_success_url())

            else:
                messages.error(request, 'Email is not registered')
                return redirect(self.get_url())
        return render(request, self.template_name, {'form': form})

def send_email_verification(request, user):
    """
    Send email verification
    """
    token = email_verification_token.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    domain = request.get_host()
    protocol = 'https' if request.is_secure() else 'http'
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
