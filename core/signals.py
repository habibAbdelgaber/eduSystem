"""
Core Signals
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create the user profile when a user is created
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_delete, sender=User)
def user_profile_deleted(sender, instance, **kwargs):
    """
    Delete the user profile when a user is deleted
    """
    try:
        instance.profile.delete()
    except UserProfile.DoesNotExist:
        pass
    
