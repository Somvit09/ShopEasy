from django.contrib import admin
from .models import Accounts
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'full_name', 'username')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Accounts, AccountAdmin)
