"""
Core admin
"""

from django.contrib import admin

from core.models import User, UserProfile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    """
    User admin
    """

    list_display = (
        'username',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
