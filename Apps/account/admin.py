from django.contrib import admin

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
        ('Identification', {'fields': ('username', 'password', 'is_active', 'is_staff')}),
        ('Personal Information', {'fields': ('email', 'first_name', 'last_name', 'phone', 'birth_date',
                                             'profile_picture')}),
        ('Complementary Information', {'fields': ('country', 'user_condition_is_read',)})
    )


admin.site.register(User, CustomerUserAdmin)
