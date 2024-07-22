from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import User, OneTimePassword
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','interests' , 'phone', 'gender')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'phone', 'gender',  'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)

    def change_password_link(self, obj):
        return format_html('<a href="{}">Change Password</a>', reverse('password-reset'))

    change_password_link.short_description = 'Password Reset'




admin.site.register(User, UserAdmin)
admin.site.register(OneTimePassword)

