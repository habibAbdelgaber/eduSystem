"""
Overriding Django's Backend Authentication System
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailBackend(ModelBackend):
    """
    Custom Email Backend
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate the user either by email or username
        """
        User = get_user_model()
        if username is None:
            # username = kwargs.get('email')
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            user = get_user_model().objects.get(
                Q(username=username) | Q(email=username)
            )
        except get_user_model().DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """
        Return the user object for the given user id
        """
        try:
            return get_user_model().objects.get(user_id=user_id)
        except get_user_model().DoesNotExist:
            return None
