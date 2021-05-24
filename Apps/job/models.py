from uuid import uuid4

from autoslug import AutoSlugField
from django.db import models

# Create your models here.
from django_countries.fields import CountryField
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField

from Apps.account.models import User
from Apps.core.models import BaseModel, PublishableModel
from BeakHub import settings


class CategoryManager(models.Manager):
    def available(self):
        return self.get_queryset().filter(status='published')


class Category(PublishableModel):
    name = models.CharField(
        verbose_name='Name',
        max_length=150,
        unique=True
    )
    slug = AutoSlugField(
        populate_from='name',
        unique=True,
        verbose_name='Slug'
    )

    objects = CategoryManager()

    class Meta:
        app_label = 'job'
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Job(models.Model):
    slug = AutoSlugField(
        populate_from='full_name',
        verbose_name='Slug'
    )
    token = models.UUIDField(
        default=uuid4,
        editable=False
    )
    title = models.CharField(
        verbose_name='Title',
        max_length=150
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True, null=True
    )
    user = models.OneToOneField(
        User,
        related_name='jobs',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    category = models.ManyToManyField(
        Category,
        blank=True,
        related_name='jobs',
        verbose_name='Categories'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is activated ?'
    )
    link_facebook = models.URLField(
        null=True, blank=True,
        verbose_name='Facebook link'
    )
    link_instagram = models.URLField(
        null=True, blank=True,
        verbose_name='Instagram link'
    )
    link_linkedin = models.URLField(
        null=True, blank=True,
        verbose_name='LinkdeIn profile link'
    )
    link_snapchat = models.URLField(
        null=True, blank=True,
        verbose_name='Link snapchat account'
    )
    link_telegram = models.URLField(
        null=True, blank=True,
        verbose_name='Telegram link'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Date created'
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date updated'
    )

    def __str__(self):
        return self.full_name

    class Meta:
        app_label = 'job'
        ordering = ('title',)
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    @property
    def full_name(self):
        return '{} {}'.format(
            self.user.username,
            self.title
        ).strip()


class PhoneNumber(models.Model):
    phone = PhoneNumberField(
        blank=True, null=True,
        verbose_name='Phone Number'
    )
    country = CountryField(
        default=settings.DEFAULT_COUNTRY,
        verbose_name='Countries'
    )
    has_whatsapp = models.BooleanField(
        default=False,
        verbose_name='Is used for WhatsApp ?'
    )
    discuss_link = models.URLField(
        blank=True, null=True,
        verbose_name='Link for WhatsApp discuss'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Activated ?'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='+'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Date created'
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date updated'
    )

    def __str__(self):
        return '({}) {}'.format(self.country.code, self.phone)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.has_whatsapp:
            self.discuss_link = 'https://wa.me/{}'.format(self.phone)
        super().save()

    class Meta:
        app_label = 'job'
        verbose_name = 'Phone Number'
        verbose_name_plural = 'Phone Numbers'
        ordering = ['phone']


class EmailAddress(models.Model):
    email = models.EmailField(
        verbose_name='Email Address'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Activated ?'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='+'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Date created'
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date updated'
    )

    def __str__(self):
        return '{}'.format(self.email)

    class Meta:
        app_label = 'job'
        verbose_name = 'Email'
        verbose_name_plural = 'Email'
        ordering = ['email']
