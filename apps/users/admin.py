from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'phone_number',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'email',
        'username',
        'phone_number',
    )
    list_filter = (
        'is_staff',
        'is_active',
    )
    readonly_fields = (
        'is_staff',
    )

    fieldsets = (
        (None, {'fields': (
            'username', 'email', 'phone_number',
            'full_name', 'birthdate', 'address', 'password',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
