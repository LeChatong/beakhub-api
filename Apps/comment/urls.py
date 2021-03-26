from django.urls import path

from Apps.comment.views import CommentJobDetailsView, CommentJobCreateListView

urlpatterns = [
    path(r'job/', CommentJobCreateListView.as_view(), name='comment-job-create-list'),
    path(r'job/<str:pk>/', CommentJobDetailsView.as_view(), name='comment-job-detail'),
]
