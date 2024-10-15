"""
Core apps
"""

from django.apps import AppConfig

class CoreConfig(AppConfig):
    """
    Core app config
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        This method is called when the app is ready
        """
