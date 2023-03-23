from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserConfig(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'username', 'date_joined', 'is_staff', 'is_active')
    list_display_links = ('id', 'email', 'username',)
    search_fields = ('username', 'email',)
    list_filter = ('is_staff', 'is_active', )
    ordering = ('-is_staff',)

    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )


admin.site.register(CustomUser, CustomUserConfig)
