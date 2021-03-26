from django.db.models import Q
from rest_framework import generics, status
from django.shortcuts import render, get_list_or_404

# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters import rest_framework as drf_filters

from Apps.account.models import User
from Apps.comment.models import CommentJob
from Apps.comment.serializers import CommentJobSerializer
from Apps.core.permissions import UserHasAPIKey
from Apps.job.models import Job


class CommentJobFilter(drf_filters.FilterSet):
    search = drf_filters.CharFilter()

    class Meta:
        model = CommentJob
        fields = [
            'job_id',
            'user_id',
        ]


class CommentJobCreateListView(generics.ListCreateAPIView):
    permission_classes = []
    serializer_class = CommentJobSerializer
    queryset = CommentJob.objects.available()
    filterset_class = CommentJobFilter

    def get_queryset(self):
        qs = super().get_queryset()

        search = self.request.query_params.get('search', None)
        job_id = self.request.query_params.get('job_id', None)
        user_id = self.request.query_params.get('user_id', None)

        if job_id:
            qs = qs.filter(job_id=job_id)

        if user_id:
            qs = qs.filter(user_id=user_id)

        if search:
            qs = qs.filter(
                Q(commentary__icontains=search)
            )
        return qs

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            get_list_or_404(
                self.get_queryset()
            ),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        commentary = request.data.get('commentary', None)
        job_id = request.data.get('job_id', None)
        user_id = request.data.get('user_id', None)

        if commentary is None:
            return Response({'error': 'The \'Commentary\' is mandatory'}, status.HTTP_400_BAD_REQUEST)
        if user_id is None:
            return Response({'error': 'The \'User\' is mandatory'}, status.HTTP_400_BAD_REQUEST)
        if job_id is None:
            return Response({'error': 'The \'Job\' is mandatory'}, status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'This user not found'}, status.HTTP_404_NOT_FOUND)
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'This job not found'}, status.HTTP_404_NOT_FOUND)

        comment = CommentJob(
            job=job,
            user=user,
            commentary=commentary
        )
        comment.save()
        serializer = self.get_serializer(
            comment,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentJobDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = CommentJobSerializer
    queryset = CommentJob.objects.all()

    def get(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(
            get_object_or_404(
                self.get_queryset(),
                pk=pk
            ),
            many=False,
            context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk=None, *args, **kwargs):
        try:
            comment = CommentJob.objects.get(pk=pk)

            commentary = request.data.get('commentary', None)
            user_id = request.data.get('user_id', None)
            job_id = request.data.get('job_id', None)
            is_active = request.data.get('is_active', None)

            if commentary:
                comment.commentary = commentary
                comment.save()
            if user_id:
                comment.user_id = user_id
                comment.save()
            if job_id:
                comment.job_id = job_id
                comment.save()
            if is_active:
                comment.is_active = is_active
                comment.save()
            serializer = self.get_serializer(
                comment,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CommentJob.DoesNotExist:
            return Response({'error': 'This Comment not found'}, status.HTTP_404_NOT_FOUND)
