from django.contrib import admin

# Register your models here.
from rest_framework_api_key.admin import APIKeyModelAdmin

from Apps.core.models import UserAPIKey


class UserAPIAdmin(APIKeyModelAdmin):
    model = UserAPIKey


admin.site.register(UserAPIKey, UserAPIAdmin)
