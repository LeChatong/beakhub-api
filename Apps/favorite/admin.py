from django.contrib import admin

# Register your models here.
from Apps.favorite.models import FavoriteJob


class FavoriteJobAdmin(admin.ModelAdmin):
    model = FavoriteJob


admin.site.register(FavoriteJob, FavoriteJobAdmin)
