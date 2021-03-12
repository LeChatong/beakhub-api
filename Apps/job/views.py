from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import render, get_list_or_404
from django_filters import rest_framework as drf_filters

# Create your views here.
from Apps.account.models import User
from Apps.core.permissions import UserHasAPIKey
from Apps.job.models import Category, Job
from Apps.job.serializers import CategorySerializer, JobSerializer


class CategoryListView(generics.ListAPIView):
    permission_classes = [UserHasAPIKey]
    serializer_class = CategorySerializer
    queryset = Category.objects.available()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            get_list_or_404(
                self.queryset
            ),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class CategoryDetailsView(generics.RetrieveAPIView):
    permission_classes = [UserHasAPIKey]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(
            get_object_or_404(
                self.get_queryset(),
                pk=pk
            ),
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class JobFilter(drf_filters.FilterSet):
    search = drf_filters.CharFilter()

    class Meta:
        model = Job
        fields = [
            'user_id',
            'category_id',
        ]


class JobListCreateView(generics.ListCreateAPIView):
    permission_classes = [UserHasAPIKey]
    serializer_class = JobSerializer
    filterset_class = JobFilter
    queryset = Job.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search', None)
        user_id = self.request.query_params.get('user_id', None)
        category_id = self.request.query_params.get('category_id', None)

        if user_id:
            qs = qs.filter(user_id=user_id)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(category__name__icontains=search)
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
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        user_id = request.data.get('user_id', None)
        category_id = request.data.get('category_id', None)

        if title is None:
            return Response({'error': 'The \'Title\' is mandatory'}, status.HTTP_400_BAD_REQUEST)
        if description is None:
            return Response({'error': 'The \'Description\' is mandatory'}, status.HTTP_400_BAD_REQUEST)
        if user_id is None:
            return Response({'error': 'The \'User\' is mandatory'}, status.HTTP_400_BAD_REQUEST)
        if category_id is None:
            return Response({'error': 'The \'Category\' is mandatory'}, status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'This user not found'}, status.HTTP_404_NOT_FOUND)
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({'error': 'This category not found'}, status.HTTP_404_NOT_FOUND)

        job = Job(
            title=title,
            description=description,
            user=user,
            category=category
        )
        job.save()
        serializer = self.get_serializer(
            job,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = [UserHasAPIKey]
    serializer_class = JobSerializer
    queryset = Job.objects.all()

    def get(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(
            get_object_or_404(
                self.get_queryset(),
                pk=pk
            ),
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, pk=None, *args, **kwargs):
        try:
            job = Job.objects.get(pk=pk)

            title = request.data.get('title', None)
            description = request.data.get('description', None)
            user_id = request.data.get('user_id', None)
            category_id = request.data.get('category_id', None)
            is_active = request.data.get('is_active', None)

            if title:
                job.title = title
                job.save()
            if description:
                job.description = description
                job.save()
            if user_id:
                job.user_id = user_id
                job.save()
            if category_id:
                job.category_id = category_id
                job.save()
            if is_active:
                job.is_active = is_active
                job.save()
            serializer = self.get_serializer(
                job,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({'error': 'This Job not found'}, status.HTTP_404_NOT_FOUND)
