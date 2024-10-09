"""
Core models
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractUser):
    """
    Custom User Model
    """

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_('User ID'),
        db_index=True,
    )
    username = models.CharField(
        _('Username'), blank=True, max_length=150, unique=True, null=True
    )
    email = models.EmailField(
        _('Email'),
        unique=True,
    )

    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        """
        String representation of the User model
        """
        return f'{self.username}' if self.username else f'{self.email}'

    def get_absolute_url(self):
        """
        Get absolute url of the User model based on the reverse
        """
        return reverse('core:user-update', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        """
        Get absolute url of the of the User model based on the reverse
        """
        return reverse('core:user-account-deletion', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        Custom save method
        """
        if self.username is None or self.username == '':
            self.username = self.email.split('@')[0].split('.')[
                0
            ]  # noga: ARGO002
            count = 0
            while User.objects.filter(username=self.username).exists():
                self.username = f'{self.username}{count}'
                count += 1

        super().save(*args, **kwargs)

def user_profile_picture(instance, filename):
    """
    Function to handle the profile picture uploads
    """
    # TODO: add a check for the file extension
    return f'users/{instance.user_id}/{filename}'

class UserProfile(models.Model):
    """
    User Profile model
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('UserProfile'),
    )

    bio = models.TextField(
        _('Bio'),
        blank=True,
        null=True,
    )
    img = models.ImageField(
        _('Image'),
        upload_to='profile_pics',
        blank=True,
        null=True,
        default='https://via.placeholder.com/100x100x.jpg',
    )

    def __str__(self):
        """
        String representation of the UserProfile model
        """
        return f'{self.user.username}'  # noga: ARGO002
