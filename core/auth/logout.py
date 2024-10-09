from django.conf import settings
from django.contrib import auth, messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import RedirectView

class LogOutView(RedirectView, SuccessMessageMixin):
    """
    Logout View
    """

    success_message = (
        'You have now logged out! Thank you for using our application'
    )
    permanent = False  # Use temporary redirect (302)

    def get_redirect_url(self):
        return reverse(
            'core:login'
        )  # Just return the URL, RedirectView handles HttpResponseRedirect

    def post(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(self.request, self.success_message)
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        request.session.flush()  # Clear the session

        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie(settings.SESSION_COOKIE_NAME)
        # print(response.cookies)
        return response
