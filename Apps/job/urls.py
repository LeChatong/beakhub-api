from django.urls import path

from Apps.job.views import (
    CategoryListView,
    CategoryDetailsView,
    JobListCreateView,
    JobDetailsView
)

urlpatterns = [
    path(r'', JobListCreateView.as_view(), name='job-create-list'),
    path(r'<str:pk>/', JobDetailsView.as_view(), name='job-detail'),
    path(r'categories/', CategoryListView.as_view(), name='category-list'),
    path(r'categories/<str:pk>/', CategoryDetailsView.as_view(), name='category-detail'),
]