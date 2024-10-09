from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy 
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import RedirectView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_encode
import requests
from requests_oauthlib import OAuth2Session
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from core.tokens import email_verification_token
class GoogleAuthenticationView(RedirectView):
    """
    Google authentication view
    """
    permanent = False
    #query_string = True
    def get_redirect_url(self, *args, **kwargs):
        """
        Get redirect url
        """
        callback = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri=https://2f8112c9-cb1b-440c-ae1b-6e29351a4060-00-dbccepdzye9t.picard.replit.dev/core/oauth/callback/&scope=email"
        return callback


class GoogleAuthenticationCallbackView(View):
  """
  Google authentication callback view
  """
  def get(self, request, *args, **kwargs):
      """
      Get request
      """
      code = request.GET.get('code')
      if not code:
          # If no code is provided, return an error or redirect
          messages.error(request, _('Authorization code not found.'))
          return redirect('core:login')

      token = "https://accounts.google.com/o/oauth2/token"
      payload = {
          "code": code,
          "client_id": settings.GOOGLE_CLIENT_ID,
          "client_secret": settings.GOOGLE_CLIENT_SECRET,
          "redirect_uri": 'https://2f8112c9-cb1b-440c-ae1b-6e29351a4060-00-dbccepdzye9t.picard.replit.dev/core/oauth/callback/',
          "grant_type": "authorization_code",
      }
      response = requests.post(token, data=payload)

      if response.status_code != 200:
          messages.error(request, _('Failed to get access token.'))
          return redirect('core:login')
      
      access_token = response.json().get('access_token')
      user_info_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
      user_info_response = requests.get(user_info_url)

      if user_info_response.status_code != 200:
          messages.error(request, _('The user info response is not found or is invalid'))
          return redirect('core:login')

      first_name = user_info_response.json().get('given_name')
      last_name = user_info_response.json().get('family_name')
      email = user_info_response.json().get('email')

      if not email:
          messages.error(request, _('The credentials are invalid'))
          return redirect('core:login')

      if not get_user_model().objects.filter(email=email).exists():
          user = get_user_model().objects.create_user(email=email)
          # user.first_name = first_name
          # user.last_name = last_name
          user.is_active = False
          user.save()
          email_verification_link(request, user)
          messages.success(request, _('Your account has been created. Please check your email to verify your email address.'))
          return redirect('core:login')
      else:
          user = get_user_model().objects.get(email=email)
          if not user.is_active:
              messages.error(request, _('Your account is not verified. Please check your email to verify your email address.'))
              return redirect('core:login')
          else:
              login(request, user)
              messages.success(request, _('You have been logged in.'))
              
              return redirect('core:user-update', pk=user.pk)



def email_verification_link(request, user):
  """
  Send email verification link
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

  subject = render_to_string('core/auth/email/email_verification_subject.txt')
  subject = ''.join(subject.splitlines())
  html_message = render_to_string('core/auth/email/email_verification.html', context)
  plain_message = render_to_string('core/auth/email/email_verification.txt', context)
  msg = EmailMultiAlternatives(subject, plain_message, settings.FROM_DEFAULT_EMAIL, [user.email])
  msg.attach_alternative(html_message, 'text/html')
  msg.send()
  
      
    