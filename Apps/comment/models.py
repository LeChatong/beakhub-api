from django.db import models

# Create your models here.
from Apps.account.models import User
from Apps.job.models import Job


class CommentManager(models.Manager):

    def available(self):
        return self.get_queryset().filter(is_active=True)


class CommentJob(models.Model):

    commentary = models.TextField(
        verbose_name='Commentary',
        null=False, blank=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='+'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is activated ?'
    )
    created_on = models.DateTimeField(
        verbose_name='Created on',
        auto_now_add=True,
        editable=False
    )
    updated_on = models.DateTimeField(
        verbose_name='Updated on',
        auto_now_add=True
    )

    objects = CommentManager()

    class Meta:
        app_label = 'comment'
        ordering = ('user', 'job', 'updated_on',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
