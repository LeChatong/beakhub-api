from django.contrib import admin

# Register your models here.
from Apps.job.models import Category, Job


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display_links = ('slug',)
    list_display = ('slug', 'name', 'status',)
    fieldsets = (
        (None, {'fields': ('name', 'status',)}),
    )


class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display_links = ('slug',)
    list_display = ('slug', 'title', 'user', 'category', 'is_active', 'created_at', 'updated_at',)
    fieldsets = (
        ('Job Information', {'fields': ('title', 'description', 'is_active',)}),
        ('Complementary Information', {'fields': ('user', 'category',)}),
    )
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Job, JobAdmin)
