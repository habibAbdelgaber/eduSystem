# from io import StringIO
import sys

from django.conf import settings
# from django.test.utils import get_runner
from django.core import management
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from core.utils import get_absolute_login_uri

# import os

class Command(BaseCommand):
    help = 'Run Django Custom Apps Tests'

    def handle(self, *args, **options):
        CUSTOM_APPS = [
            app.split('.')[0] for app in getattr(settings, 'CUSTOM_APPS', [])
        ]
        if not CUSTOM_APPS:
            self.stdout.write(
                self.style.ERROR(
                    'CUSTOM_APPS is not defined in settings.py. Make sure to add it and try again.'
                )
            )
            sys.exit(1)

        # output = StringIO()
        # sys.stdout = output

        try:
            management.call_command(
                'test',
                CUSTOM_APPS,
                verbosity=0,
                interactive=False,
                traceback=False,
            )

        except (SystemExit, Exception) as e:
            self.stdout.write(self.style.ERROR(f'Test Failed: {e}' + '\n'))
            sys.exit(1)

        # results = output.getvalue()
        subject = 'Django Test Passed'
        message = f'Django test for custom apps have passed successfully!\n{get_absolute_login_uri()}'
        if not getattr(settings, 'FROM_DEFAULT_EMAIL', None):
            self.stdout.write(
                self.style.ERROR(
                    'FROM_DEFAULT_EMAIL is not defined in settings.py. Make sure to add it and try again.'
                )
            )

        send_mail(
            subject,
            message,
            'noreply@gmail.com',
            [settings.FROM_DEFAULT_EMAIL],
            fail_silently=False,
        )

        self.stdout.write(
            self.style.SUCCESS('Django test for custom apps have passed')
        )
