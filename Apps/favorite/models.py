from django.db import models

# Create your models here.
from Apps.account.models import User
from Apps.job.models import Job


class FavoriteManager(models.Manager):

    def are_in_the_favorites(self):
        return self.get_queryset().filter(has_liked=True)


class FavoriteJob(models.Model):
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
    has_liked = models.BooleanField(
        default=True,
        verbose_name='Has liked ?'
    )
    updated_on = models.DateTimeField(
        verbose_name='Updated on',
        auto_now_add=True
    )

    objects = FavoriteManager()

    class Meta:
        app_label = 'favorite'
        ordering = ('user', 'job', 'updated_on',)
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
