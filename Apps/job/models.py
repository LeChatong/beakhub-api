from autoslug import AutoSlugField
from django.db import models

# Create your models here.
from Apps.account.models import User
from Apps.core.models import BaseModel, PublishableModel


class Category(BaseModel):
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
        unique=True,
        verbose_name='Slug'
    )
    title = models.CharField(
        verbose_name='Title',
        max_length=150
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True
    )
    user = models.ForeignKey(
        User,
        related_name='jobs',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    category = models.ForeignKey(
        Category,
        related_name='jobs',
        on_delete=models.CASCADE,
        verbose_name='Category'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is activated ?'
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
        ordering = ('title', 'category',)
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    @property
    def full_name(self):
        return '{} {}'.format(
            self.user.username,
            self.title
        ).strip()