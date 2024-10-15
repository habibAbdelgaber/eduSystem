"""
Core utils
"""

from django.conf import settings
from django.urls import reverse

def get_absolute_login_uri():
    """
    Build and return the absolute URI for the login page
    """
    allow_hosts = settings.ALLOWED_HOSTS

    allow_hosts = [host.strip() for host in allow_hosts]

    if allow_hosts:
        host = allow_hosts[0]

    else:
        host = 'localhost'

    ORIGIN = '2f8112c9-cb1b-440c-ae1b-6e29351a4060-00-dbccepdzye9t.picard'
    SCHEME = 'https' if not settings.SECURE_SSL_REDIRECT else 'http'
    BASE_URL = f'/{SCHEME}://{ORIGIN}{host}'

    LOGIN_URL = reverse('core:login')
    ABSOLUTE_URI = f'{BASE_URL}{LOGIN_URL}'
    return ABSOLUTE_URI
