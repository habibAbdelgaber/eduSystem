"""
Core tasks
"""

import sys
from io import StringIO

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.management import call_command

def developers_email(subject, message):
    """
    Send an email to the developers
    """
    # Get the user model
    User = get_user_model()
    # Get the developers
    developers = User.objects.filter(is_staff=True)
    # Send the email
    for developer in developers:
        send_mail(
            subject,
            message,
            settings.FROM_DEFAULT_EMAIL,
            [developer.email],
            fail_silently=False,
        )

@shared_task
def run_tests():
    """
    Run tests.
    """
    test_output = StringIO()
    sys.stdout = test_output

    try:
        call_command('test', verbosity=2)

    except Exception as e:
        sys.stderr.write(str(e))

        sys.stderr.write('\n')

    sys.stdout = sys.__stdout__

    test_output.seek(0)
    results = test_output.read()
    return developers_email(
        subject='Tests',
        message=f'Tests results: {results}',
        # context={'results': results},
    )
