from django.urls import path

from Apps.favorite.views import FavoriteJobDetailsView, FavoriteJobCreateListView

urlpatterns = [
    path(r'job/', FavoriteJobCreateListView.as_view(), name='fav-job-create-list'),
    path(r'job/<str:pk>/', FavoriteJobDetailsView.as_view(), name='fav-job-detail'),
]
