from django.contrib import admin

# Register your models here.
from Apps.job.models import Category


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display_links = ('slug')
    list_display = ('slug', 'name',)
    fieldsets = (
        (None, {'fields': ('name',)})
    )
