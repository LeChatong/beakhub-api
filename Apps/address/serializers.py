from django.contrib.sites.models import Site
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from Apps.address.models import Country, City, Zone
from BeakHub import settings


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='country-detail'
    )
    flag = SerializerMethodField()

    class Meta:
        model = Country
        fields = [
            'url',
            'id',
            'name',
            'code',
            'is_active',
            'flag',
            'phone_prefix'
        ]

    def get_flag(self, obj):
        if obj.flag:
            site = Site.objects.get(pk=settings.SITE_ID)
            return site.domain + obj.flag
        return None


class CitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='city-detail'
    )
    country = CountrySerializer(many=False)

    class Meta:
        model = City
        fields = [
            'url',
            'id',
            'name',
            'is_active',
            'country'
        ]


class ZoneSerializer(serializers.HyperlinkedModelSerializer):

    city = CitySerializer(many=False)

    class Meta:
        model = Zone
        fields = [
            'url',
            'id',
            'name',
            'is_active',
            'city'
        ]
