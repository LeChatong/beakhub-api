from rest_framework import serializers

from Apps.favorite.models import FavoriteJob


class FavoriteJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteJob
        fields = '__all__'
