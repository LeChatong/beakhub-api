from django.urls import path

from Apps.account.views import UserListView, UserDetailsView, UserDetailsByUsernameView, UserDetailsByEmailView

urlpatterns = [
    path(r'', UserListView.as_view(), name='user-create'),
    path(r'<str:pk>/', UserDetailsView.as_view(), name='user-details'),
    path(r'username/<str:username>/', UserDetailsByUsernameView.as_view(), name='user-details-by-username'),
    path(r'email/<str:email>/', UserDetailsByEmailView.as_view(), name='user-details-by-email')
]