from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import FormView
from django.core.mail import send_mail
from django.urls import reverse_lazy

from core.forms import ContactUsForm

class ContactUsView(FormView):
    """
    Contact us view
    """

    template_name = 'core/auth/email/contactus.html'
    form_class = ContactUsForm

    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact us'
        context['header'] = 'Get in touch with us'
        context['form_type'] = 'contactus'
        context['action'] = 'Contact Us'
        return context

    def form_valid(self, form):
        """
        Form valid
        """
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        email = form.cleaned_data.get('email')
        name = form.cleaned_data.get('name')
        send_mail(
            subject,
            message,
            settings.FROM_DEFAULT_EMAIL,
            [email],
            fail_silently=False,
        )
        messages.success(
            self.request,
            f'Hi {name}, Thank you for getting in touch us. We will get back to you soon.',
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Form invalid
        """
        messages.error(
            self.request, 'Something went wrong. Please try again later.'
        )
        return super().form_invalid(form)
