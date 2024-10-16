"""
Core tokens
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Custom Token Generator
    """

    def _make_hash_value(self, user, timestamp):
        """
        Make the hash value
        """
        return (
            six.text_type(user.pk) \
            + six.text_type(timestamp) \
            + six.text_type(user.is_active)
        )


email_verification_token = TokenGenerator()
