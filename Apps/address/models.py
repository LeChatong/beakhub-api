from django.db import models

# Create your models here.
from django_countries.fields import Country as CountryType, CountryField
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE

from Apps.job.models import Job


class PlaceManager(models.Manager):

    def activated(self):
        return self.get_queryset().filter(
            is_active=True
        )


class Country(models.Model):
    country = CountryField(
        unique=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is activated ?'
    )

    objects = PlaceManager()

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('country',)
        unique_together = ('country',)

    @property
    def name(self):
        if isinstance(self.country, CountryType):
            return self.country.name
        return str(self.country)

    @property
    def code(self):
        if isinstance(self.country, CountryType):
            return self.country.code
        return self.country

    @property
    def flag(self):
        if isinstance(self.country, CountryType):
            return self.country.flag
        return self.country

    @property
    def phone_prefix(self):
        for code, isos in COUNTRY_CODE_TO_REGION_CODE.items():
            if self.code in isos:
                return '+' + str(code)
        return None

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='name'
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is activated ?'
    )

    objects = PlaceManager()

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ('country', 'name',)
        unique_together = ('country', 'name',)

    @property
    def full_name(self):
        return '{}, {}'.format(
            self.name,
            self.country.name
        )

    def __str__(self):
        return self.full_name


class Zone(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='name'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='zones'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is activated ?'
    )

    objects = PlaceManager()

    class Meta:
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'
        ordering = ('city__country', 'city__name', 'name',)
        unique_together = ('city', 'name',)

    def __str__(self):
        return '{}, {}'.format(
            self.name,
            self.city.full_name
        )
