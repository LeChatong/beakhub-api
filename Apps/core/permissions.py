from rest_framework_api_key.permissions import BaseHasAPIKey

from Apps.core.models import UserAPIKey


class UserHasAPIKey(BaseHasAPIKey):
    model = UserAPIKey
