from django.db import models

# Create your models here.
from django.db.models import Q
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField
from model_utils.models import TimeStampedModel
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager


class BaseModel(TimeStampedModel):
    class Meta:
        abstract = True


class PublishableManager(models.Manager):

    def published(self):
        return self.get_queryset().filter(Q(status='published'))

    def draft(self):
        return self.get_queryset().filter(Q(status='draft'))

    def removed(self):
        return self.get_queryset().filter(Q(status='removed'))


class PublishableModel(BaseModel):
    STATUS = Choices(
        ('draft', 'draft'),
        ('published', 'published'),
        ('removed', 'removed')
    )
    status = StatusField()
    status_changed = MonitorField(monitor='status')

    objects = PublishableManager()

    class Meta:
        abstract = True


class UserAPIKey(AbstractAPIKey):

    objects = BaseAPIKeyManager()

    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
