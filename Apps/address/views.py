from rest_framework import generics, status
from django.shortcuts import render, get_list_or_404

# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters import rest_framework as drf_filters

from Apps.address.models import Country, City, Zone
from Apps.address.serializers import CountrySerializer, CitySerializer, ZoneSerializer
from Apps.core.permissions import UserHasAPIKey


class CountryListView(generics.ListAPIView):
    permission_classes = [UserHasAPIKey]
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
    permission_classes = [UserHasAPIKey]
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
    permission_classes = [UserHasAPIKey]
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
    permission_classes = [UserHasAPIKey]
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
    permission_classes = [UserHasAPIKey]
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
    permission_classes = [UserHasAPIKey]
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
