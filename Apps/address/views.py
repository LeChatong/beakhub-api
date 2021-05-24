from rest_framework import generics, status
from django.shortcuts import render, get_list_or_404

# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters import rest_framework as drf_filters

from Apps.address.models import Country, City, Zone, Address
from Apps.address.serializers import CountrySerializer, CitySerializer, ZoneSerializer, AddressSerializer
from Apps.core.permissions import UserHasAPIKey
from Apps.job.models import Job


class CountryListView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CountrySerializer
    queryset = Country.objects.activated()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            get_list_or_404(
                self.get_queryset()
            ),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class CountryDetailView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = CountrySerializer
    queryset = Country.objects.activated()

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


class CityFilter(drf_filters.FilterSet):
    class Meta:
        model = City
        fields = [
            'country_id'
        ]


class CityListView(generics.ListAPIView):
    permission_classes = []
    serializer_class = CitySerializer
    queryset = City.objects.activated()
    filterset_class = CityFilter

    def get_queryset(self):
        qs = super().get_queryset()
        country_id = self.request.query_params.get('country_id', None)
        if country_id:
            qs = qs.filter(country_id=country_id)
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


class CityDetailView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = CitySerializer
    queryset = City.objects.activated()

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


class ZoneFilter(drf_filters.FilterSet):
    country_id = drf_filters.NumberFilter()

    class Meta:
        model = Zone
        fields = [
            'city_id',
        ]


class ZoneListView(generics.ListAPIView):
    permission_classes = []
    serializer_class = ZoneSerializer
    filterset_class = ZoneFilter
    queryset = Zone.objects.activated()

    def get_queryset(self):
        qs = super().get_queryset()
        country_id = self.request.query_params.get('country_id', None)
        city_id = self.request.query_params.get('city_id', None)
        if country_id:
            cities_id = []
            cities = City.objects.activated().filter(country_id=country_id)
            for city in cities:
                cities_id.append(city.id)
            qs = qs.filter(city_id_in=cities_id)
        if city_id:
            qs = qs.filter(city_id=city_id)
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


class ZoneDetailsView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = ZoneSerializer
    queryset = Zone.objects.activated()

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


class AddressFilter(drf_filters.FilterSet):
    user_id = drf_filters.NumberFilter()

    class Meta:
        model = Address
        fields = [
            'job_id',
            'zone_id',
        ]


class AddressListCreateView(generics.ListCreateAPIView):
    permission_classes = []
    serializer_class = AddressSerializer
    filterset_class = AddressFilter
    queryset = Address.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()

        job_id = self.request.query_params.get('job_id', None)
        zone_id = self.request.query_params.get('zone_id', None)
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            jobs_id = []
            jobs = Job.objects.all().filter(user_id=user_id)
            for job in jobs:
                jobs_id.append(job.token)
            qs = qs.filter(job_token_in=jobs_id)
        if zone_id:
            qs = qs.filter(zone_id=zone_id)
        if job_id:
            qs = qs.filter(job_id=job_id)
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
        is_active = request.data.get('is_active', None)
        description = request.data.get('description', None)
        job_id = request.data.get('job_id', None)
        zone_id = request.data.get('zone_id', None)

        if job_id is None:
            return Response({'error': 'The job is mandatory'}, status.HTTP_400_BAD_REQUEST)

        try:
            job = Job.objects.get(token=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'The job not found'}, status.HTTP_404_NOT_FOUND)

        if zone_id is None:
            return Response({'error': 'The zone is mandatory'}, status.HTTP_400_BAD_REQUEST)

        try:
            zone = Zone.objects.get(token=job_id)
        except Zone.DoesNotExist:
            return Response({'error': 'The zone not found'}, status.HTTP_404_NOT_FOUND)

        if description is None:
            return Response({'error': 'The description is mandatory'}, status.HTTP_400_BAD_REQUEST)

        address = Address(
            job=job,
            zone=zone,
            description=description,
            is_active=is_active
        )
        address.save()

        serializer = self.get_serializer(
            address,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddressDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = []
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

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
            address = Address.objects.get(pk=pk)

            is_active = request.data.get('is_active', None)
            description = request.data.get('description', None)
            job_id = request.data.get('job_id', None)
            zone_id = request.data.get('zone_id', None)

            if job_id:
                address.job_id = job_id
                address.save()

            if zone_id:
                address.zone_id = zone_id
                address.save()

            if description:
                address.description = description
                address.save()

            if is_active:
                address.is_active = is_active
                address.save()

            serializer = self.get_serializer(
                address,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({'error': 'The Address not found.'}, status.HTTP_404_NOT_FOUND)

