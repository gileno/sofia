from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, ResetPassword
from .forms import UserAdminForm, AdminUserChangeForm, AdminUserCreationForm


class UserAdmin(BaseUserAdmin):

    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email')}),
        (
            _('Permissions'), {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser', 'groups',
                    'user_permissions'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    list_display = ('username', 'email', 'name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'name', 'email')


class ResetPasswordAdmin(admin.ModelAdmin):

    list_display = ['user', 'key', 'confirmed_on']


admin.site.register(User, UserAdmin)
admin.site.register(ResetPassword, ResetPasswordAdmin)
