from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer

from Apps.account.serializers import UserSerializer
from Apps.job.models import Category, Job, PhoneNumber, EmailAddress


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class JobSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='job-detail'
    )
    user = UserSerializer(many=False)

    class Meta:
        model = Job
        fields = [
            'url',
            'token',
            'slug',
            'title',
            'description',
            'is_active',
            'user',
            'created_at',
            'updated_at'
        ]


class PhoneNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneNumber
        fields = '__all__'


class EmailAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailAddress
        fields = '__all__'
