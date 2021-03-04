from django.urls import path

from Apps.account.views import UserListView, UserCreateView

urlpatterns = [
    path(r'', UserCreateView.as_view(), name='user-create'),
    path(r'list', UserListView.as_view(), name='user-list')
]