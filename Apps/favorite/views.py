from django.shortcuts import render, get_list_or_404

# Create your views here.
from rest_framework import generics, status
from django_filters import rest_framework as drf_filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from Apps.account.models import User
from Apps.favorite.models import FavoriteJob
from Apps.favorite.serializers import FavoriteJobSerializer
from Apps.job.models import Job


class FavoriteJobFilter(drf_filters.FilterSet):

    class Meta:
        model = FavoriteJob
        fields = [
            'job_id',
            'user_id',
        ]


class FavoriteJobCreateListView(generics.ListCreateAPIView):
    permission_classes = []
    serializer_class = FavoriteJobSerializer
    queryset = FavoriteJob.objects.are_in_the_favorites()
    filterset_class = FavoriteJobFilter

    def get_queryset(self):
        qs = super().get_queryset()

        job_id = self.request.query_params.get('job_id', None)
        user_id = self.request.query_params.get('user_id', None)

        if job_id:
            qs = qs.filter(job_id=job_id)

        if user_id:
            qs = qs.filter(user_id=user_id)

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
        job_id = request.data.get('job_id', None)
        user_id = request.data.get('user_id', None)

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

        fav = FavoriteJob(
            job=job,
            user=user,
            has_liked=True
        )
        fav.save()
        serializer = self.get_serializer(
            fav,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavoriteJobDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = FavoriteJobSerializer
    queryset = FavoriteJob.objects.all()

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
            fav = FavoriteJob.objects.get(pk=pk)

            user_id = request.data.get('user_id', None)
            job_id = request.data.get('job_id', None)
            has_liked = request.data.get('has_liked', None)

            if user_id:
                fav.user_id = user_id
                fav.save()
            if job_id:
                fav.job_id = job_id
                fav.save()
            if has_liked:
                fav.has_liked = has_liked
                fav.save()
            serializer = self.get_serializer(
                fav,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FavoriteJob.DoesNotExist:
            return Response({'error': 'This Favorite not found'}, status.HTTP_404_NOT_FOUND)
