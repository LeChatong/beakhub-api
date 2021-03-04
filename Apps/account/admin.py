from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from Apps.account.models import User


class CustomerUserAdmin(UserAdmin):
    model = User

    list_filter = ('country', 'is_staff', 'is_active', 'date_joined', 'date_update')

    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_active', 'activation_key', 'is_staff',
                    'date_joined',)

    ordering = ('date_joined', 'username',)

    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone',)

    fieldsets = (
        (_('Identification'), {'fields': ('username', 'password', 'is_active', 'is_staff', 'activation_key')}),
        (_('Personal Information'), {'fields': ('email', 'first_name', 'last_name', 'phone', 'birth_date',
                                                'profile_picture')}),
        (_('Complementary Information'), {'fields': ('country', 'user_condition_is_read', 'date_joined',
                                                     'date_update')})
    )


admin.site.register(User, CustomerUserAdmin)
