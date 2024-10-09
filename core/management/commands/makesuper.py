from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = _('Create a Super user')
    
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
              username='admin',
              email='admin@gmail.com',
              password='admin54321'
            )
            user.is_instructor = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Super user created for: {user.username} successfully'))
            
        else:
          self.stdout.write(self.style.ERROR(_('Superuser already exists.')))
        